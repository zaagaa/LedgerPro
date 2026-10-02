import os
import django

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BusinessApp.settings")
django.setup()

from django.apps import apps
from django.db.models import ForeignKey
from inventory.models import Inventory

# Step 1: Get all Inventory IDs
all_inventory_ids = set(Inventory.objects.values_list('id', flat=True))

# Step 2: Find all models using ForeignKey to Inventory
used_inventory_ids = set()

for model in apps.get_models():
    for field in model._meta.get_fields():
        if isinstance(field, ForeignKey) and field.related_model == Inventory:
            try:
                values = model.objects.values_list(field.name, flat=True).distinct()
                used_inventory_ids.update(filter(None, values))



            except Exception as e:
                print(f"Error accessing {model.__name__}.{field.name}: {e}")

# Step 3: Find unused inventory IDs
unused_ids = all_inventory_ids - used_inventory_ids
unused_inventories = Inventory.objects.filter(id__in=unused_ids)

# Step 4: Print unused inventories
print(f"\nFound {unused_inventories.count()} unused inventory records:\n")
for inv in unused_inventories:
    print(f"ID: {inv.id}, Name: {inv.inventory_name}")

# Step 5: Ask for confirmation before deleting
if unused_inventories.exists():
    confirm = input("\nDo you want to delete these unused inventory records? (yes/no): ").strip().lower()
    if confirm == "yes":
        deleted_count = unused_inventories.delete()[0]
        print(f"\n Deleted {deleted_count} inventory records.")
    else:
        print("\n❌ Deletion aborted.")
else:
    print("\n No unused inventory found.")
