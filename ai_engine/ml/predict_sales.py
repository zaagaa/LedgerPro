import os
import datetime
import joblib
import pandas as pd
from django.conf import settings
from django.db.models import Sum
from invoice.models import Invoice

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "ai_engine",
    "ml",
    "models",
    "sales_model.pkl"
)

def predict_tomorrow_sales():

    model = joblib.load(MODEL_PATH)

    # Get recent data
    qs = (
        Invoice.objects
        .values('invoice_date__date')
        .annotate(total=Sum('total_amount'))
        .order_by('-invoice_date__date')[:7]
    )

    df = pd.DataFrame(qs)

    df.rename(columns={
        'invoice_date__date': 'date',
        'total': 'sales'
    }, inplace=True)

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    prev_day_sales = df['sales'].iloc[-1]
    last_7_days_avg = df['sales'].mean()

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    input_data = [[
        tomorrow.day,
        tomorrow.month,
        tomorrow.weekday(),
        prev_day_sales,
        last_7_days_avg
    ]]

    prediction = model.predict(input_data)[0]

    return {
        "date": tomorrow,
        "prediction": round(max(prediction, 0), 2)
    }