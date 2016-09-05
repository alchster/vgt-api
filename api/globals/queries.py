QUERIES = dict(
        create_carclass = "{carClassCode}, '{carClassName}'",

        create_city = "'{cityName}', {cityTZDeltaSeconds}",
  
        create_place = "'{placeCity}', '{placeName}', {placeType}",

        create_address = "'{addressPlace}', '{addressStreet}', "\
            "'{addressHouse}', '{addressPorch}', '{addressInfo}'",

        create_passenger = "'{passengerPhone}', '{passengerName}', "\
            "'{passengerPatronymic}', '{passengerSurname}', "\
            "'{passengerDescription}'",

        create_order = "{orderID}, {orderPartnerID}, {orderManagerID}, "\
            "'{orderCreateDateTime}', '{orderFeedbackURL}'",

        create_service = "'{_order}', {serviceID}, {serviceType}, "\
            "{serviceStatus}, {serviceCarClassID}, {servicePassengersCount}, "\
            "'{serviceMeetDateTime}', '{serviceMeetPlate}', "\
            "'{serviceBaggage}', {serviceBabyChairs}, '{serviceComment}'",

        add_address_to_service = "'{serviceID}', '{addressID}', {serial}",

        add_passenger_to_service = "'{serviceID}', '{passengerID}', {serial}"
    )
