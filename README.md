# Multi-Objective Optimisation Applied to the Electoral Division Problem in Ireland

## Overview

In this project, an **evolutionary algorithm** was implemented in Python in order to evolve the current configuration of the constituency boundaries in Ireland towards a new configuration which better satisfied the criteria specified in the Irish Constitution. The configurations were generated randomly by switching boundary electoral divisions from one constituency to another, and their adherence to the specified criteria was evaluated using a reward function to determine the optimal configuration. The Pandas library was used for data analysis, while the GeoPandas library was used to apply geometric methods such as intersections and differences to spatial data.

## Introduction

On 9 February 2023, a new state body called the Electoral Commission was established to oversee elections in Ireland.[^1] One of the key roles of the Electoral Commission is reviewing the the Dáil Éireann constituencies, and making a report and recommendations in relation to possible changes to constituency boundaries.[^2] In making these recommendations, the Commission is required to observe the following provisions of the Constitution:

- Article 16.2.2˚ of the Constitution provides that:

>The number of members shall from time to time be fixed by law, but the total number of members of Dáil Éireann shall not be fixed at less than one member for each thirty thousand of the population, or at more than one member for each twenty thousand of the population.

- Article 16.2.3˚ of the Constitution provides that:

>The ratio between the number of members to be elected at any time for each constituency and the population of each constituency, as ascertained at the last preceding census, shall, so far as it is practicable, be the same throughout the country.

In addition to these requirements, the Commission must have regard to the following:

1. the total number of members of the Dáil, subject to Article 16.2.2° of the Constitution, shall be **not less than 171 and not more than 181**;

2. each constituency shall return **3, 4 or 5 members**;

3. the **breaching of county boundaries** shall be avoided as far as practicable.  

4. each constituency shall be composed of **contiguous** areas;

5. there shall be regard to geographic considerations including significant physical features and the extent of and the density of population in each constituency; and

6. subject to the above matters, the Commission shall endeavour to maintain **continuity** in relation to the arrangement of constituencies.

*The reference in (3) above to county boundaries is deemed not to include a reference to the boundary of a city or any boundary between any two of the counties of Dún Laoghaire-Rathdown, Fingal and South Dublin.*

Ireland is divided up into 3,440 electoral divisions (EDs), which are currently split between 39 constituencies. The constituencies can be changed by transferring EDs from one constituency to another. The large number of constraints imposed by the Constitution mean that determining the optimal constituency boundaries is a challenging problem. In this project, numerical methods were implemented in order to find a solution which better satisfied the requirements and recommendations set out above.

[^1]: [Irish Government Press Release](https://www.gov.ie/en/press-release/fd25a-an-coimisiun-toghchain-the-electoral-commission-is-formally-established-on-a-statutory-footing/)
[^2]: [Electoral Commission: Constituency Reviews](https://www.electoralcommission.ie/constituency-reviews/)
