import os
import pymysql

# Connect to the database
db = pymysql.connect(host=os.getenv("DATABASE_HOST"), user=os.getenv('DATABASE_USERNAME'),
                     password=os.getenv('DATABASE_PASSWORD'), autocommit=True, ssl_ca= "/etc/ssl/cert.pem")


try:
    # Create a cursor to interact with the database
    cursor = db.cursor()

    # cursor.execute("CREATE TABLE `genome_scores` (`movieID` INT NOT NULL,`tagID` INT NOT NULL, `relevance` float(20) NOT NULL);")
    cursor.execute("CREATE TABLE `genome_tags` (`tagID` INT NOT NULL,`tag` VARCHAR(1000) NOT NULL,PRIMARY KEY (`tagID`));")
    cursor.execute("CREATE TABLE `rating_explicit` (`userID` INT NOT NULL,`tmdbID` INT NOT NULL,`rating` FLOAT NOT NULL,`timestamp` VARCHAR(50) NULL);")
    cursor.execute("CREATE TABLE `ml_youtube` (`youtubeID` VARCHAR(100) NOT NULL,`movieID` INT NOT NULL);")
    cursor.execute("CREATE TABLE `movies` (`movieID` INT NOT NULL AUTO_INCREMENT,`title` VARCHAR(200) NOT NULL,`release_year` VARCHAR(20),`overview` VARCHAR(2000),PRIMARY KEY (`movieID`));")
    cursor.execute("CREATE TABLE `movie_imdb_tmdb` (`movieID` INT NOT NULL,`imdbID` INT NULL,`tmdbID` INT NOT NULL UNIQUE);")
    cursor.execute("CREATE TABLE `genres` (`genreID` INT NOT NULL, `genre_name` VARCHAR(45) NOT NULL,PRIMARY KEY (`genreID`));")
    cursor.execute("CREATE TABLE `movie_genres` ( `movieID` INT NOT NULL,`genreID` INT NOT NULL);")
    cursor.execute("CREATE TABLE `users` (`userID` INT NOT NULL AUTO_INCREMENT,`name` VARCHAR(100) NULL,`age` INT ,`email` VARCHAR(100) , `password` VARCHAR(100) ,PRIMARY KEY (`userID`));")
    cursor.execute("CREATE TABLE `rating_implicit` (`userID` INT NOT NULL,`tmdbID` INT NOT NULL,`interaction` INT NOT NULL,`timestamp` VARCHAR(50));")
    cursor.execute("CREATE TABLE `user_movielist` (`userID` INT NOT NULL,`tmdbID` INT NOT NULL);")
    cursor.execute("CREATE TABLE `daily_update` ( `tmdbID` INT NOT NULL,`title` VARCHAR(100) NOT NULL,`type` VARCHAR(100) NOT NULL,`date` DATE DEFAULT (CURRENT_DATE));")
    cursor.execute("CREATE TABLE `models_type` (`modelID` INT NOT NULL,`modelType` VARCHAR(45) NOT NULL,PRIMARY KEY (`modelID`));")
    cursor.execute("CREATE TABLE `kryptonite`.`user_recommendations` (`userID` INT NOT NULL,`tmdbID` INT NOT NULL,`modelID` INT NOT NULL,`timestamp` DATETIME NULL);")
    cursor.execute("ALTER TABLE `kryptonite`.`movies` CHANGE COLUMN `movieID` `movieID` INT NOT NULL AUTO_INCREMENT ;")
    cursor.execute("ALTER TABLE `kryptonite`.`users` CHANGE COLUMN `userID` `userID` INT NOT NULL AUTO_INCREMENT ;")
    cursor.execute("ALTER TABLE  `user_recommendations` ADD CONSTRAINT ur_userID_fk FOREIGN KEY (userID) REFERENCES users (userID) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE `user_recommendations` ADD CONSTRAINT ur_tmdbID_fk FOREIGN KEY (tmdbID) REFERENCES movie_imdb_tmdb (tmdbID) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE `user_recommendations` ADD CONSTRAINT ur_modelID_fk FOREIGN KEY (modelID) REFERENCES models_type (modelID) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE `genome_scores` ADD CONSTRAINT gs_tagID_fk FOREIGN KEY (tagID) REFERENCES genome_tags (tagID) ON DELETE CASCADE; ")
    cursor.execute("ALTER TABLE `genome_scores` ADD CONSTRAINT gs_movieID_fk FOREIGN KEY (movieID) REFERENCES movies (movieID) ON DELETE CASCADE; ")
    cursor.execute("ALTER TABLE `movie_genres` ADD CONSTRAINT mg_movieID_fk FOREIGN KEY (movieID) REFERENCES movies (movieID) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE movie_genres ADD CONSTRAINT mg_genreID_fk FOREIGN KEY (genreID) REFERENCES genres (genreID) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE ml_youtube ADD CONSTRAINT ml_movieID_fk FOREIGN KEY (movieID) REFERENCES movies (movieID) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE rating_explicit ADD CONSTRAINT rs_tmdbID_fk FOREIGN KEY (tmdbID) REFERENCES movie_imdb_tmdb (tmdbID) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE rating_explicit ADD CONSTRAINT rs_userID_fk FOREIGN KEY (userID) REFERENCES users (userID) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE rating_implicit ADD CONSTRAINT rss_tmdbID_fk FOREIGN KEY (tmdbID) REFERENCES movie_imdb_tmdb (tmdbID) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE rating_implicit ADD CONSTRAINT rss_userID_fk FOREIGN KEY (userID) REFERENCES users (userID) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE movie_imdb_tmdb ADD CONSTRAINT mit_movie_fk FOREIGN KEY (movieID) REFERENCES movies (movieID) ON DELETE CASCADE; ")
    cursor.execute("ALTER TABLE user_movielist ADD CONSTRAINT uml_user_fk FOREIGN KEY (userID) REFERENCES users (userID) ON DELETE CASCADE; ")
    cursor.execute("ALTER TABLE user_movielist ADD CONSTRAINT uml_tmdb_fk FOREIGN KEY (tmdbID) REFERENCES movie_imdb_tmdb (tmdbID) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE daily_update ADD CONSTRAINT du_tmdb_fk FOREIGN KEY (tmdbID) REFERENCES movie_imdb_tmdb (tmdbID) ON DELETE CASCADE;")


    # Execute "SHOW TABLES" query
    cursor.execute("Show TABLES")

    # Fetch all the rows
    tables = cursor.fetchall()

    # Print out the tables
    print("Tables in the database:")
    for table in tables:
        print(table[0])

except pymysql.Error as e:
    print("MySQL Error:", e)

finally:
    # Close the cursor and connection
    cursor.close()
    db.close()
