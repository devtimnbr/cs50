-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Get all crime scenes for that specific date - found 2 mentioning Humphrey Street (one about littering so no theft), the theft was witnessed by 3 people
SELECT * FROM crime_scene_reports WHERE year = 2021 AND day = 28 AND month = 7;

-- Get the transcriptions for that specific date - Ruth, Raymond and Eugene seem to be the witnesses
SELECT name, transcript FROM interviews WHERE year = 2021 AND day = 28 AND month = 7;

-- Found 2 Eugene's in the transcriptions - check if it's the same person
SELECT name FROM people WHERE name = 'Eugene';

-- Found only 1 Eugene - so it's the same person with 2 transcriptions for that date

-- Eugene mentions that the he so the thief withdrawing money at Leggett Street on that date
SELECT * FROM atm_transactions WHERE year = 2021 AND day = 28 AND month = 7 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'; 

-- Found 8 withdraw transactions on that date and atm - checking the names for the bank accounts
SELECT name, atm_transactions.account_number, atm_transactions.amount FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE year = 2021 AND day = 28 AND month = 7 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'; 

-- Raymond mentions that the thief called someone and they were lanning to take the earliest flight out of Fiftyville the next day. Figurring out flights.
SELECT flights.id, destination_airport_id, hour, minute FROM flights
JOIN airports ON airports.id = flights.origin_airport_id
WHERE airports.city = 'Fiftyville' AND year = 2021 AND day = 29 AND month = 7 ORDER BY hour, minute;

-- The first flight is at 8:20 with flight id of 36. Get the city of the destination airport of id 4
SELECT city, full_name FROM airports WHERE id = 4;

-- The flights goes to New York City | LaGuardia Airport. Get the passenger list of that flight
SELECT name, passengers.passport_number, passengers.seat, passengers.flight_id FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
JOIN flights ON flights.id = passengers.flight_id
WHERE flights.id = 36;

-- Found 8 passengers. Check the phone call registry to get the suspects. The call waas under 1 minute
-- First check all callers
SELECT phone_calls.id, name, passport_number, phone_number FROM people 
JOIN phone_calls ON phone_calls.caller = phone_number
WHERE year = 2021 AND day = 28 AND month = 7 and phone_calls.duration <= 60;

-- Check all receivers
SELECT phone_calls.id, name, passport_number, phone_number FROM people 
JOIN phone_calls ON phone_calls.receiver = phone_number
WHERE year = 2021 AND day = 28 AND month = 7 and phone_calls.duration <= 60;

-- Ruth mentioned the the thief drove away within 10 minuted from the theft - check license plates for that timeframe around 10:15am
SELECT name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.activity = 'exit' 
AND bakery_security_logs.year = 2021 AND bakery_security_logs.day = 28 AND bakery_security_logs.month = 7 
AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute >= 10 AND bakery_security_logs.minute <= 25;


-- Bruce can be found in every data entry
-- Bruce called with Robin and escaped to NYC