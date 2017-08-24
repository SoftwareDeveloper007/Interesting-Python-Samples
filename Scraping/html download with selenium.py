def download_selenium(url, num_retries=3):

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
    except:
        if num_retries > 0:
            driver.close()
            download_selenium(url, num_retries-1)

    return driver