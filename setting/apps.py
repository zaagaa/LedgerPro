from django.apps import AppConfig
from django.db.models.signals import post_delete, post_migrate
from django.db.utils import OperationalError, ProgrammingError


class SettingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'setting'

    def ready(self):
        try:
            from pos.models import Print_Template

            default_template_content = """var qr_image=`<img style="width:150px;" src="{% url 'qr_code' data='123' %}" alt="QR Code">`;
qr_image=qr_image.replace("123",response.qrcode_data);

html += `<table class="content" border="0" cellpadding="5" cellspacing="5" style="width:69mm;">
<tbody>
<tr><td colspan="5" style="white-space: nowrap;">{{pos_header|safe}}</td></tr>`;

if(response.headline){
html+=`<tr><td colspan="5" class="text-center" style="font-weight:bold;white-space: nowrap;">`+response.headline+`</td></tr>`;
}

html+=`<tr>
<td style="text-align:center;border-bottom: 1px solid black;" colspan="5">
<span style="float:left;">BILL NO: `+ response.invoice_number + `</span>
<span style="float:right;">DT: `+ response.invoice_date + `</span>
</td>
</tr>
<tr>
<th style="width:10mm;border-bottom: 1px solid black;">PRICE</th>
<th style="text-align:left;width:100%;border-bottom: 1px solid black;">ITEM</th>
<th style="border-bottom: 1px solid black;">UNIT</th>
<th style="border-bottom: 1px solid black;">QTY</th>
<th style="border-bottom: 1px solid black;text-align:right;">AMOUNT</th>
</tr>`;

$(response.sale_data).each(function (index, value) {
    row_tax = parseFloat(value.tax_amount) - (parseFloat(value.tax_amount) * (parseFloat(response.total_discount_percent) / 100));
    gross = parseFloat(value.gross_sale_price) - (parseFloat(value.gross_sale_price) * (parseFloat(response.total_discount_percent) / 100));

    html += `<tr>
<td>`+ value.sale_price + `</td>
<td style="font-size:9px;"><b>`+ value.inventory_name + `</b></td>
<td style="text-align:center;">`+ value.unit + `</td>
<td style="text-align:center;">`+ value.qty + `</td>
<td style="text-align:right;">`+ value.amount + `</td>
</tr>
<tr>
<td colspan="5"><small><code>CGST: `+ (row_tax / 2).toFixed(2) + ` (` + value.tax_rate / 2 + `%) | SGST: ` + (row_tax / 2).toFixed(2) + ` (` + value.tax_rate / 2 + `%)<br>` + gross.toFixed(2) + ` + ` + (row_tax / 2).toFixed(2) + ` + ` + (row_tax / 2).toFixed(2) + ` = ` + (parseFloat(gross) + parseFloat(row_tax)).toFixed(2) + `</code></small></td>
</tr>`;
});

html += `<tr>
<th style="border-top: 1px solid black;text-align:right;" colspan="2">TOTAL:</th>
<th style="border-top: 1px solid black;text-align:center;">`+ response.total_unit + `</th>
<th style="border-top: 1px solid black;text-align:center;">`+ response.total_qty + `</th>
<th style="border-top: 1px solid black;text-align:right;">`+ response.total_amount + `</th>
</tr>`;

if (response.total_discount != 0) {
    html += `<tr>
<th style="border-top: 1px solid black;text-align:right;" colspan="4">Discount :</th>
<th style="border-top: 1px solid black;text-align:right;">`+ response.total_discount + `</th>
</tr>`;
}

if (response.round_off!=null && response.round_off!=0) {
    html += `<tr>
<th style="border-top: 1px solid black;text-align:right;" colspan="4">Round Off :</th>
<th style="border-top: 1px solid black;text-align:right;">`+ response.round_off + `</th>
</tr>`;
}

if (response.total_discount != 0) {
    html += `<tr>
<th style="border-top: 1px solid black;text-align:right;" colspan="4">GRAND TOTAL:</th>
<th style="border-top: 1px solid black;text-align:right;">`+ response.invoice_total_amount + `</th>
</tr>`;
}

html += `<tr><td colspan="5"><br></td></tr>
<tr><td style="border: 1px solid black;text-align:center;" colspan="5"><h3>GRAND TOTAL: Rs.`+ response.invoice_total_amount + `/-</h3></td></tr>
<tr><td colspan="5"><center><code style="font-size:10px;">`+ response.total_gross_amount + `+` + (response.total_tax_amount / 2).toFixed(2) + `(CGST)+` + (response.total_tax_amount / 2).toFixed(2) + `(SGST)=` + (response.total_amount - response.total_discount) + `</code></center></td></tr>
<tr><td colspan="5"><center>CASHIER: `+ response.username + `</center></td></tr>`;

let balance = 0;
html += `<tr><td colspan="5">BILL AMOUNT: `+ response.invoice_total_amount + `</td></tr>`;

if (response.cash) {
    html += `<tr><td colspan="5">CASH PAID: `+ response.cash + `</td></tr>`;
    balance += response.cash;
}
if (response.card) {
    html += `<tr><td colspan="5">CARD PAID: `+ response.card + `</td></tr>`;
    balance += response.card;
}
if (response.upi) {
    html += `<tr><td colspan="5">UPI PAID: `+ response.upi + `</td></tr>`;
    balance += response.upi;
}
if (response.credit) {
    html += `<tr><td colspan="5">CREDIT: `+ response.credit + `</td></tr>`;
    balance += response.credit;
}

html += `<tr><td colspan="5">BALANCE: `+ (balance - response.invoice_total_amount) + `</td></tr>
<tr><td colspan="5" style="white-space: nowrap;">{{pos_footer|safe}}</td></tr>
<tr><td colspan="5"><center><span style="font-weight:bold;font-size:24px;">`+ response.qrcode_data + `</span><br>` + qr_image + `</center></td></tr>
</tbody></table>`;"""

            # Ensure pk=1 template exists or create
            try:
                template = Print_Template.objects.filter(pk=1).first()
                if not template or not template.template:
                    Print_Template.objects.update_or_create(
                        pk=1,
                        defaults={
                            'template_name': 'Default',
                            'template': default_template_content
                        }
                    )
            except ProgrammingError:
                pass

            # Recreate if pk=1 is deleted
            def recreate_template(sender, instance, **kwargs):
                if instance.pk == 1:
                    Print_Template.objects.update_or_create(
                        pk=1,
                        defaults={
                            'template_name': 'Default',
                            'template': default_template_content
                        }
                    )

            post_delete.connect(recreate_template, sender=Print_Template)

            # Signal: setup default settings
            from .signals import setup_default_settings
            post_migrate.connect(setup_default_settings, sender=self)

        except OperationalError:
            pass
