import aiosqlite


# =================================
# Initialize the Database
# =================================
async def init_db():
    async with aiosqlite.connect("level.db") as connect:

        connect.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                UserId TEXT PRIMARY KEY,
                XP INT DEFAULT 0,
                Level INT DEFAULT 1
            )
        """)

        # save the changes
        await connect.commit()


# =================================
# Add XP to User in Database
# =================================
async def Adding_Xp(UserId, Amount):
    # Open a connection to the database for this operation
    async with aiosqlite.connect("Level.db") as connect:

        # retrieve the xp and level using the UserID
        async with connect.execute("SELECT XP, Level FROM Users WHERE UserId = ?", (str(UserId),)) as cursor:
            result = await cursor.fetchone()     # fetch one row from the query

            # If the user exists
            if result:
                XP, Level = result
                XP += Amount

                # craete a level-up depending on the amount of XP required

                # update the database with new XP
                cursor.execute("UPDATE Users SET XP = ?, Level = ? WHERE UserId = ?", (XP, Level, UserId))
            else:
                # if the user doesn't exist then add them to DB
                cursor.execute("INSERT INTO Users (UserId, XP) VALUES (?, ?)", (UserId, Amount))

            await connect.commit()

        







