-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Get crime scene Discription
SELECT description FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";

-- 1. Theft took place at 10:15 am.
-- 2. 3 witnesses, all mentions the bakery.

-- Getting the transcripts
SELECT name, transcript FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%Bakery%";

-- 1. License number in securtiy log, within 10 mintues of the theft.
-- 2. The thief withdrew cash from ATM on Leggett Street in the morning.
-- 3. He talked to his accomplise from less than a minute after stealing.
-- 4. He probably took the earliest flight on 29 June leving Fiftyville.

-- Getting the thief
SELECT * from people

WHERE id IN

(SELECT person_id FROM bank_accounts WHERE account_number IN
    (SELECT account_number FROM atm_transactions
    WHERE year = 2021 AND month = 7 AND day = 28 AND
    atm_location = "Leggett Street" AND transaction_type = "withdraw"))

AND phone_number IN

(SELECT caller FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)

AND license_plate IN

(SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND
minute BETWEEN 15 AND 25 AND activity = "exit")

AND passport_number IN

(SELECT passport_number from passengers
WHERE flight_id IN
    (SELECT id FROM flights WHERE origin_airport_id =
        (SELECT id FROM airports WHERE city = "Fiftyville")
    AND year = 2021 AND month = 7 AND day = 29
    ORDER BY hour, minute LIMIT 1));

--+--------+-------+----------------+-----------------+---------------+
--|   id   | name  |  phone_number  | passport_number | license_plate |
--+--------+-------+----------------+-----------------+---------------+
--| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
--+--------+-------+----------------+-----------------+---------------+

-- Getting the city

SELECT city FROM airports WHERE id =
    (SELECT destination_airport_id FROM flights
        WHERE id =
        (SELECT flight_id FROM passengers WHERE passport_number = 5773159633));

-- The thief flew to New York City

-- Getting the accomplice

SELECT * from people WHERE phone_number =
    (SELECT receiver FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
    AND caller = "(367) 555-5533");

-- +--------+-------+----------------+-----------------+---------------+
--|   id   | name  |  phone_number  | passport_number | license_plate |
--+--------+-------+----------------+-----------------+---------------+
--| 864400 | Robin | (375) 555-8161 | NULL            | 4V16VO0       |
--+--------+-------+----------------+-----------------+---------------+