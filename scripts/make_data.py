import sys
import os
import pandas as pd

import cianparser


got_deal_type = ""
got_location  = ""
got_homeowner = ""
got_rooms     = []


def get_all_locations() :
    """Печать доступных локаций
    :return: ничего
    """

    lst = cianparser.list_cities()
    lst = [i[0] for i in lst]

    print("\nВСЕ ДОСТУПНЫЕ МЕСТА:")
    for item in lst :
        print(item)
    print()


def get_data(rms) :
    """Генерация списка данных
    :param rms: тип квартиры
    :return: список данных
    """

    global got_deal_type, got_location, got_rooms, got_homeowner

    data = cianparser.parse(
        deal_type          = got_deal_type,
        accommodation_type = "flat",
        location           = got_location,
        rooms              = rms,
        start_page         = 1,
        end_page           = 1,     # 100000
        is_saving_csv      = False, # True
        is_latin           = False,
        is_express_mode    = False,
        is_by_homeowner    = got_homeowner
    )

    return data


def get_df(deal_type, location, rooms, is_by_homeowner) :
    """Создание датасета
    :param deal_type: тип объявления
    :param location: населенный пункт
    :param rooms: тип квартиры
    :param is_by_homeowner: тип автора объявления
    :return: ничего
    """

    global got_deal_type, got_location, got_rooms, got_homeowner

    got_deal_type = deal_type
    got_location  = location
    got_homeowner = is_by_homeowner
    got_rooms     = rooms.split(",")
    got_rooms     = [i.replace(" ", "") for i in got_rooms]

    for i in range( len(got_rooms) ) :

        print( "Получаем данные для количества комнат = {0}:".format(got_rooms[i]) )

        if (i == 0) :

            if got_rooms[i].isdigit () :
                lst_data  = get_data( int(got_rooms[i]) )
            else :
                lst_data  = get_data(got_rooms[i])

        else :

            if got_rooms[i].isdigit () :
                lst_tmp  = get_data( int(got_rooms[i]) )
            else:
                lst_tmp  = get_data(got_rooms[i])

            lst_data = lst_data + lst_tmp

    col_names = ["author", "author_type", "link", "city", "deal_type",
                 "accommodation_type", "floor", "floors_count", "rooms_count",
                 "total_meters", "price_per_m2", "price_per_month", "commissions",
                 "year_of_construction", "living_meters", "kitchen_meters",
                 "phone", "district", "street", "underground"]
    df_data   = pd.DataFrame(lst_data, columns=col_names)

    try:
        os.ulink("../../data/raw/data.csv")
    except:
        print("Error while deleting file")

    df_data.to_csv(r'../../data/raw/data.csv', index=False)
