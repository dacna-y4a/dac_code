from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import random

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

# Create DAG
dag = DAG(
    'quote_and_hello_dag',
    default_args=default_args,
    description='DAG with quote fetcher and hello world tasks',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['example', 'quotes', 'hello'],
)

def get_and_print_quote():
    """
    Task để lấy một câu quote ngẫu nhiên và in ra
    """
    try:
        # Sử dụng API miễn phí để lấy quote
        response = requests.get('https://api.quotable.io/random')
        if response.status_code == 200:
            quote_data = response.json()
            quote = quote_data.get('content', 'No quote found')
            author = quote_data.get('author', 'Unknown')
            
            print(f"📝 Quote of the day:")
            print(f"'{quote}' - {author}")
            
            return f"Quote: {quote} - {author}"
        else:
            # Fallback quotes nếu API không hoạt động
            fallback_quotes = [
                "The only way to do great work is to love what you do. - Steve Jobs",
                "Innovation distinguishes between a leader and a follower. - Steve Jobs", 
                "Life is what happens when you're busy making other plans. - John Lennon",
                "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
                "It is during our darkest moments that we must focus to see the light. - Aristotle"
            ]
            selected_quote = random.choice(fallback_quotes)
            print(f"📝 Quote of the day (fallback):")
            print(selected_quote)
            return f"Fallback quote: {selected_quote}"
            
    except Exception as e:
        print(f"Error fetching quote: {e}")
        # Fallback quote nếu có lỗi
        fallback_quote = "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill"
        print(f"📝 Quote of the day (error fallback):")
        print(fallback_quote)
        return f"Error fallback quote: {fallback_quote}"

def hello_world():
    """
    Task đơn giản để in Hello World
    """
    message = "🌍 Hello World from Airflow DAG!"
    print(message)
    print("This is a simple hello world task.")
    print("Task executed successfully! ✅")
    return message

# Task 1: Lấy và in quote
quote_task = PythonOperator(
    task_id='get_quote_task',
    python_callable=get_and_print_quote,
    dag=dag,
)

# Task 2: Hello World
hello_task = PythonOperator(
    task_id='hello_world_task',
    python_callable=hello_world,
    dag=dag,
)

# Thiết lập dependency: chạy song song (không phụ thuộc lẫn nhau)
# Nếu muốn chạy tuần tự: quote_task >> hello_task
# Hiện tại để song song để tối ưu thời gian thực thi
quote_task
hello_task
