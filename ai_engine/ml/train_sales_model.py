import os
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from django.db.models import Sum
from invoice.models import Invoice
from django.conf import settings

MODEL_DIR = os.path.join(settings.BASE_DIR, "ai_engine", "ml", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "sales_model.pkl")

def train_sales_model():

    os.makedirs(MODEL_DIR, exist_ok=True)

    qs = (
        Invoice.objects
        .values('invoice_date__date')
        .annotate(total=Sum('total_amount'))
        .order_by('invoice_date__date')
    )

    df = pd.DataFrame(qs)

    if df.empty:
        print("No invoice data found!")
        return

    df.rename(columns={
        'invoice_date__date': 'date',
        'total': 'sales'
    }, inplace=True)

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # Feature Engineering
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.weekday

    # 🔥 NEW FEATURES
    df['prev_day_sales'] = df['sales'].shift(1)
    df['last_7_days_avg'] = df['sales'].rolling(window=7).mean()

    df = df.dropna()

    X = df[['day', 'month', 'weekday', 'prev_day_sales', 'last_7_days_avg']]
    y = df['sales']

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    print("✅ Improved model trained successfully!")