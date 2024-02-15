# Quantifying the Success of Long-Term Contracts in Major League Baseball

## Author Information:
**CSC-475 Project Proposal**  
**Author:** Caden Parry  
**Department:** Department of Computer Science, Furman University  
**Email:** caden.parry@furman.edu  

- **Caden Parry**
- **Email:** caden.parry@furman.edu  

## Background
In December of 2023, Japanese superstar Shohei Ohtani signed a massive 10-year 700 million dollar contract with the Los Angeles Dodgers, the largest in sports history. While Shohei Ohtani’s contract is a definitive outlier, the baseball world has become increasingly accustomed to seeing contracts totaling hundreds of millions of dollars. As a result of these lucrative signings many fans and executives alike are tasked with answering the question, "Was all of that money with it?"

## Goal
This research will work to provide a quantitative measure to determine how successful a contract was based on the dollar amount invested. Common one-to-one statistical player comparison is already a complex and subjective task, but the financial burden of a large contract is often removed from the equation. A database or easily accessible reference tool housing this data could serve as a beneficial resource for fans, journalists, and MLB executives.

## Data
To complete this research, I will leverage Baseball-Reference.com’s yearly player batting statistics[1] and WAR statistics [2], as well as Spotrac.com’s player contract data [3] and player statistics data [4]. All Baseball-Reference data can easily be exported to Excel but data from Spotrac will likely need to be acquired using a web-scraper. Data collection from Spotrac is player-specific but the population size of players with 100 million dollar or more contracts is relatively small.

## Methods
To answer this question, I plan to use a statistical analysis that compares a given player’s cost per point of WAR (wins above replacement - this is a statistic that determines how many more wins a given player generated than a replacement level player) with the average cost per point of WAR throughout all of Major League Baseball [5]. For example, if player A costs 10 million dollars and he generates 1 WAR, he would be valued at 10 million dollars/1 WAR. If the league average cost to produce 1 WAR is 2.5 million dollars (2.5 million dollars/1 WAR), then player A’s contract would be overvalued. While the statistical method I plan to use in this project is not original, my project will add value by expanding its breadth to new players and increasing accessibility. Many of these calculations are locked behind paywalls or are located deep in a given website. This project will work to produce a simple and user-friendly tool to visualize this data for the public.

## Evaluation
Success for this project can be quantified by the size of the final database of player and their given attributes. The value of this project lies in the breadth and accessibility of the final product, and thus, the larger and more scalable the dataset the better. Ideally, this analysis could be expanded to every player, past and present, but for this project, I would view a finished website with a database of 50 players as a success.

## Dissemination
To disseminate this project, I plan to create a publicly available website that will act as a visualization tool for my data. I am not currently aware of the most efficient process to create a publicly available website but I plan to leverage Furman University staff to educate me on this process. I do not plan on releasing my final report on a public server, however, dependent on the creation of a working website, I would be willing to demo my website at Furman Engaged.

## References
[1] [Baseball-Reference Batting Statistics](https://www.baseball-reference.com/leagues/majors/2023-standard-batting.shtml). [Online; accessed 25-Jan-2024].  
[2] [Baseball-Reference WAR Statistics](https://www.baseball-reference.com/leagues/majors/2023-value-batting.shtml). [Online; accessed 25-Jan-2024].  
[3] [Spotrac Player Contract Data](https://www.spotrac.com/mlb/los-angeles-dodgers/mookie-betts-15744/). [Online; accessed 25-Jan-2024].  
[4] [Spotrac Player Statistics Data](https://www.spotrac.com/mlb/los-angeles-dodgers/mookie-betts-15744/statistics/). [Online; accessed 25-Jan-2024].  
[5] Briton A Hagan. Characteristics and Success of Long-Term Contracts in Major League Baseball. PhD thesis, The University of New Mexico, 2017.
