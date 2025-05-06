from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
from tabulate import tabulate


def search_flights(origin, destination):
    # Dictionary mapping airport codes to their full name XPaths for selection
    airport_data = {
        'BLR': "//p[contains(text(),'Bangalore, IN - Kempegowda International Airport (')]",
        'DEL': "//p[normalize-space()='New Delhi, IN - Indira Gandhi Airport (DEL)']",
        'CCU': "//p[contains(text(),'Kolkata, IN - Netaji Subhas Chandra Bose Airport (')]",
        'HYD': "//p[normalize-space()='Hyderabad, IN - Rajiv Gandhi International (HYD)']",
        'MAA': "//p[normalize-space()='Chennai, IN - Chennai Airport (MAA)']"
    }
    options = webdriver.ChromeOptions()
    service = Service(executable_path="chromedriver.exe.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.cleartrip.com/")
    driver.maximize_window()
    sleep(3)


    driver.find_element(By.XPATH, "//div[@class='pb-1 px-1 flex flex-middle nmx-1']//*[name()='svg']").click()
    sleep(1)

    driver.find_element(By.XPATH, "//h2[normalize-space()='Flights']").click()

    driver.find_element(By.XPATH,
                        "//div[@class='pb-1 px-1 flex flex-middle nmx-1']//*[name()='svg']//*[name()='path' and contains(@d,'M18 6L12 1')]").click()

    driver.find_element(By.XPATH, "//input[contains(@placeholder,'Where from?')]").send_keys(origin)
    driver.find_element(By.XPATH, airport_data[origin]).click()
    sleep(1)

    driver.find_element(By.XPATH, "//input[@placeholder='Where to?']").send_keys(destination)
    driver.find_element(By.XPATH, airport_data[destination]).click()
    sleep(1)

    driver.find_element(By.XPATH, "//div[contains(text(),'Tue, May 6')]").click()
    sleep(3)
    driver.find_element(By.XPATH,
                        "/html[1]/body[1]/div[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[4]/div[1]/div[1]/div[1]/div[4]/div[3]/div[1]/div[2]/div[1]/div[3]/div[2]/div[3]/div[1]/div[1]").click()

    driver.find_element(By.XPATH,
                        "/html[1]/body[1]/div[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[4]/div[1]/div[1]/div[1]/div[3]").click()
    driver.find_element(By.XPATH,
                        "//div[@aria-label='Sat May 10 2025']//div[@class='p-1 day-gridContent fs-14 fw-500 flex flex-middle flex-column flex-center flex-top']").click()
    sleep(2)

    driver.find_element(By.XPATH, "//h4[@class='sc-gEvEer cmEgze']").click()
    sleep(10)

    # Get the Flight details
    print(f"\n--- {origin} to {destination} Flight Details ---")

    def table_format(data):
        data_split = data.strip().split('\n\n')

        flights = []
        current_flight = []
        for line in data_split[0].split('\n'):
            if line.strip() == '':
                continue
            if line in ['Enjoy free meal']:  # Skip promotional lines
                continue
            current_flight.append(line.strip())
            if len(current_flight) == 7:
                flights.append(current_flight)
                current_flight = []

        table_data = []
        i = 0
        for flight in flights:
            if i > 4:
                break
            else:
                table_data.append([
                    flight[0],  # Airline
                    flight[1],  # Flight No
                    flight[2],  # Departure
                    flight[4],  # Stops
                    flight[3],  # Duration
                    flight[5],  # Arrival
                    flight[6]  # Price
                ])
            i += 1

        headers = ["Airline", "Flight No", "Departure", "Stops", "Duration", "Arrival", "Price"]
        print(tabulate(table_data, headers=headers, tablefmt="grid", showindex=False))


    departure_flights = driver.find_elements(By.XPATH, "(//div[@data-test-attrib='onward-view'])[1]")
    print("\nDeparture Flight Details:")
    for flight in departure_flights:
        table_format(flight.text)

    return_flights = driver.find_elements(By.XPATH, "(//div[@data-test-attrib='return-view'])[1]")
    print("\nReturn Flight Details:")
    for flight in return_flights:
        table_format(flight.text)

    # Close browser
    driver.quit()


def main():
    destinations = ['DEL', 'CCU', 'HYD', 'MAA']

    # Get user input
    print("Available destinations from Bangalore (BLR):")
    print("1. Delhi (DEL)")
    print("2. Kolkata (CCU)")
    print("3. Hyderabad (HYD)")
    print("4. Chennai (MAA)")

    choice = input("\nEnter destination number (1-4) or press Enter to search all: ")

    if choice.strip() and choice in ['1', '2', '3', '4']:
        destination = destinations[int(choice) - 1]
        search_flights('BLR', destination)
    else:
        for destination in destinations:
            search_flights('BLR', destination)
            print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":
    main()

