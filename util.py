def scroll_til_element_centered(driver, element):
    desired_y = (element.size['height'] / 2) + element.location['y']
    window_h = driver.execute_script('return window.innerHeight')
    window_y = driver.execute_script('return window.pageYOffset')
    current_y = (window_h / 2) + window_y
    scroll_y_by = desired_y - current_y

    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

def american_to_decimal(price):
    if price > 0:
        return (price/100) + 1
    else:
        return abs(100 / price) + 1

def decimal_to_american(price):
    if price >= 2.0:
        return (price-1)*100
    else:
        return (-100)/(price-1)
