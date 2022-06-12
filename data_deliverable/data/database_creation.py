import sqlite3

conn = sqlite3.connect('project_data.db')
c = conn.cursor()

# c.execute('DROP TABLE IF EXISTS "ev_stocks";')
# c.execute('DROP TABLE IF EXISTS "oil_prices";')
# c.execute('DROP TABLE IF EXISTS "metal_prices";')
# c.execute('DROP TABLE IF EXISTS "lithium";')

conn.commit()
