from analytics import Research, Analytics
import config
import os

def analyze_data(file_path, has_header):
    class_instance = Research(file_path, has_header)
    data = class_instance.file_reader()
    print("Данные из файла:", data)
    calculations = Research.Calculations(data)
    heads, tails = calculations.counts() 
    print(f"Решка: {tails}, Орел: {heads}")   
    heads_percent, tails_percent = calculations.fractions(heads, tails)
    print(f"Вероятности: {tails_percent:.2f}% и {heads_percent:.2f}%")
    analytics = Analytics(data)
    predictions = analytics.predict_random(config.num_of_steps)
    print("Прогнозы на следующие шаги:", predictions)
    print(analytics.predict_last())

    pred_heads = sum(1 for p in predictions if p[0] == 1)
    pred_tails = sum(1 for p in predictions if p[0] == 0)
        
    prediction_summary = f"{pred_tails} tail and {pred_heads} heads"

    report = config.report_template.format(total=len(data), tails_count=tails, heads_count=heads, tails_percent=round(tails_percent,2), heads_percent=round(heads_percent,2), num_predictions=config.num_of_steps, prediction_summary=prediction_summary)
    print(report)  
    saved_file = analytics.save_data(report, "record")
        
    return report

if __name__ == '__main__':
    path = os.environ.get('FILE_PATH')
    has_header = os.environ.get('HAS_HEADER', 'true').lower() == 'true'
    if not path:
        command_line = ' '.join(os.sys.argv)  
        parts = command_line.split()
        if len(parts) >= 3:
            path = parts[1]
            has_header = parts[2].lower() == 'true'
        elif len(parts) == 2:
            path = parts[1]
            has_header = True
    if path and os.path.exists(path) and path.endswith('.csv'):
        report = analyze_data(path, has_header)
    else:
        print("Ошибка: неверный путь к файлу или файл не CSV")
