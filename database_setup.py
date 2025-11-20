#import redis
import pymysql.cursors
import ssl
import os

MYSQL_HOST = "anime-convention-tracker-animeconventiontracker2025.h.aivencloud.com" 
MYSQL_PORT = 26181
MYSQL_USER = "avnadmin"
MYSQL_PASSWORD = "AVNS_YbJP225UsFzOAys_79O"
DB_NAME = "defaultdb" # The default database name

data = [["Anirevo Toronto 2025","2025-11-21","2025-11-23", "Metro Toronto Convention Centre, Toronto ON","Canada","https://toronto.animerevolution.ca/"],
["Anime North 2026","2026-05-22","2026-05-24", "Toronto Congress Center / Delta Hotels by Marriott Toronto Airport & Conference Centre, Toronto ON","Canada", "https://www.animenorth.com/"],
["Calgary Anime-Fest 2026","2026-04-04","2026-04-04", "Radisson Hotel & Conference Centre Calgary Airport, Calgary AB","Canada","http://canadaanimefests.ca/Calgary/?utm_source=FanCons.com&utm_medium=web&utm_campaign=FanCons.com"],
["Fan Expo Canada 2026","2026-08-27","2026-08-30", "Metro Toronto Convention Centre, Toronto ON", "Canada", "https://fanexpohq.com/fanexpocanada/"],
["Anime Ottawa 2026","2026-04-03","2026-04-05", "EY Center, Ottawa ON","Canada","https://animeottawa.com/"],
["San Diego Anime Con 2025","2025-11-21","2025-11-23", "Handlery Hotel San Diego, San Diego CA","USA","https://sandiegoanimecon.com/"],
["Fan Expo San Francisco 2025","2025-11-28","2025-11-30", "Moscone Center, San Francisco CA","USA","https://fanexpohq.com/fanexposanfrancisco/"],
["Anime Washington 2026","2026-02-06","2026-02-08", "Washington State Fair and Events Center, Puyallup WA","USA","https://animewashington.com/"],
["Anime Expo 2026","2026-07-02","2026-07-05", "Los Angeles Convention Center, Los Angeles CA","USA","https://www.anime-expo.org/"],
["Anime USA 2026","2026-11-20","2026-11-22", "Westfields Marriott Washington Dulles, Chantilly VA","USA","https://animeusa.regfox.com/anime-usa-2026"],
["Kotae Expo 2025","2025-11-23","2025-11-23", "Tampere Exhibition and Sports Center, Tampere","Finland","https://kotae.fi/en/"],
["Animefest 2026","2026-05-22","2026-05-24", "Brno Exhibition Centre, Brno", "Czech Republic","https://www.animefest.cz/en"],
["HaruCon 2026","2026-05-09","2026-05-10", "Kärntner Messen Klagenfurt, Klagenfurt am Wörtherse","Austria","https://harucon.at/"],
["Animangapop Cardiff Winter 2025","2025-11-29","2025-11-29", "Future Inn Cardiff Bay, Cardiff","UK","https://animangapop.co.uk/cardiffwinter/"],
["MinamiCon 2026","2026-03-13","2026-03-13", "	Novotel Southampton, Southampton","UK","https://www.minamicon.org.uk/"],
["Lifetime Memory Eng Only 2026","2026-01-25","2026-01-25", "Yau Tsim Mong Multicultural Activity Centre, Jordan","Hong Kong","https://en.lifetimememory.info/?utm_source=AnimeCons.ca&utm_medium=web&utm_campaign=FanCons.com"],
["Comic Fiesta 2025","2025-12-20","2025-12-21", "Kuala Lumpur Convention Centre, Kuala Lumpur","Malaysia","https://comicfiesta.org/"],
["Anime Festival Asia Singapore 2025","2025-11-28","2025-11-30", "Suntec Singapore Convention & Exhibition Centre","Singapore","https://animefestival.asia/afasg25/"],
["Comic Market 2025","2025-12-30","2025-12-31", "Tokyo Big Sight, Tokyo","Japan","https://www.comiket.co.jp/info-a/TAFO/C107TAFO/index.html"],
["Tasminé Summer Festival 2026","2026-01-31","2026-01-31", "Kingborough Community Hub, Kingston Tasmania","Australia","https://www.tasmine.org/summer-festival"],
["Animethon 2026","2026-08-07","2026-08-09", "Edmonton Convention Center, Edmonton AB","Canada","https://animethon.org/"],
["Montreal Anime-Fest 2025","2025-11-22","2025-11-22", "Radisson Hotel Montreal Airport, Saint-Laurent QC","Canada","http://canadaanimefests.ca/Montreal/"],
["Otafest 2026","2026-05-15","2026-05-17", "Calgary Telus Convention Centre & Marriott Downtown, Calgary AB","Canada","https://otafest.com/"],
["Anime Japan 2026","2026-03-28","2026-03-29", "Tokyo Big Sight, Tokyo","Japan","https://anime-japan.jp/en/"],
["Sakura-Con 2026","2026-04-03","2026-04-05", "Seattle Convention Center, Seattle WA","USA","https://sakuracon.org/"],
["Anime NYC 2026","2026-08-20","2026-08-20", "Javits Convention Center, New York NY ","USA","https://animenyc.com/"]]

connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=DB_NAME,
            charset='utf8mb4',
            # Key for secure connection:
            ssl={"ssl_verify_cert": True, "ssl_ca": "aiven-ca.pem"},
            # Use DictCursor to return results as dictionaries (optional but useful)
            cursorclass=pymysql.cursors.DictCursor
        )
print("✅ Successfully connected to Aiven MySQL database!")

with connection.cursor() as cursor:
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS Conventions (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            start_date DATE,
            end_date DATE,
            location VARCHAR(255),
            country VARCHAR(100),
            url VARCHAR(255)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        
    cursor.execute(create_table_sql)
    
    print(f"✅ Table 'Conventions' checked/created successfully.")
    add_convention = """
        INSERT INTO Conventions (name, start_date, end_date, location, country, url)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    for convention in data:
        cursor.execute(add_convention, tuple(convention))
        print(f"✅ convention {convention[0]} added successfully.")
    connection.commit()


if 'connection' in locals() and connection.open:
    connection.close()