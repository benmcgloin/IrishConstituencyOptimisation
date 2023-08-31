# Multi-Objective Optimisation Applied to Electoral Redistricting in Ireland

## Overview

In 2023, the [Electoral Commission](https://www.electoralcommission.ie/constituency-reviews/) of Ireland was tasked with preparing a set of recommendations on possible changes to the constituency boundaries of Ireland. In doing so, they were required satisfy numerous criteria stipulated by the Irish Constitution, pertaining to features such as population per representative, contiguity of constituencies, and temporal continuity. The large number of objectives involved in the design of the constituency boundaries means that this is a prime use case for **multi-objective optimisation**.

In this project, an **evolutionary algorithm** was implemented in Python in order to evolve the current configuration of the constituency boundaries in Ireland towards a new configuration which better satisfied the criteria specified in the Irish Constitution. The configurations were generated randomly by switching boundary electoral divisions from one constituency to another, and their adherence to the specified criteria was evaluated using a reward function to determine the optimal configuration. The `pandas` library was used for data analysis, while the `geopandas` library was used to apply geometric methods such as intersections and differences to spatial data.

The algorithm was observed to be successful at only producing configurations with contiguous constituencies, and at producing constituencies with Seat Equivalent Representation values that were usually closer to integers than those of the constituencies in the current configuration. This meant that these altered constituencies could be more fairly represented by an actual number of elected representatives, which was the desired outcome.

<figure>
<p align="center">
  <img src="images/current_configuration_numbered.svg" style="width:800px;height:800px;"/>
</p>
<figcaption><em>The current configuration of the 39 Irish constituencies.</em></figcaption>
</figure>

## Background

On 9 February 2023, a new state body called the [Electoral Commission](https://www.electoralcommission.ie/constituency-reviews/) was [established](https://www.gov.ie/en/press-release/fd25a-an-coimisiun-toghchain-the-electoral-commission-is-formally-established-on-a-statutory-footing/) to oversee elections in Ireland. One of the key roles of the Electoral Commission is reviewing the the Dáil Éireann constituencies, and making a report and recommendations in relation to possible changes to constituency boundaries. In making these recommendations, the Commission is required to observe the following provisions of the [Irish Constitution](http://www.irishstatutebook.ie/en/constitution/index.html):

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

Ireland is divided up into 3,440 electoral divisions (EDs), which are currently split between 39 constituencies. The constituencies can be changed by transferring EDs from one constituency to another. The large number of constraints imposed by the Constitution mean that determining the optimal constituency boundaries is a challenging problem. In this project, numerical methods were implemented in order to find a solution which better satisfied the requirements and recommendations set out above.

Further details are provided in our <a href="Redistricting_Ireland_Report.pdf" type=application/pdf>report</a>.
