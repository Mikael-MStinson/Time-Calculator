def calculate_time(start,end):
    if end < start:
        end += 1200
    #slope = 10/6 
    start_minute = start%100
    end_minute = end%100
    start = start - start_minute + (start_minute * (10/6))
    end = end - end_minute + (end_minute * (10/6))
    return round((end-start)/100,2)