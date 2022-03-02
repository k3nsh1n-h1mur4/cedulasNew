import sqlite3


def con():
	con = sqlite3.connect("cedulas.sqlite")
	con.row_factory = sqlite3.Row
	if con is None:
		print("mala cone")
		return False
	elif con:
		cursor = con.cursor()
		rows = cursor.execute('SELECT * FROM cedulasTable')
		result = rows.fetchone()
		for i in result:
			print(i)

f = con


if __name__ == "__main__":
	f()