---
author:
- |
  Alexander Farren, Ben McGloin,\
  Eliza Somerville and Mikey Whelan
bibliography:
- refs.bib
title: Multi-Objective Optimisation Applied to the Electoral
  Redistricting of Ireland
---


# Introduction

In 2023, the Electoral Commission of Ireland was tasked with preparing a
set of recommendations on possible changes to the constituency
boundaries of Ireland. In doing so, they were required satisfy numerous
criteria stipulated by the Irish Constitution, pertaining to features
such as population per representative, contiguity of constituencies, and
temporal continuity. The large number of objectives involved in the
design of the constituency boundaries means that this is a prime use
case for *multi-objective optimisation*.

Multi-objective optimisation is the process of finding a solution to a
problem that best satisfies multiple objectives. While a wide variety of
techniques are available for single-objective optimisation, there are
comparatively fewer methods available for multi-objective optimisation.
One example of such a method is an evolutionary algorithm, which
involves generating solution candidates and then evolving them towards a
more optimised solution.

In this project, an evolutionary algorithm was implemented in Python
with the aim of generating a configuration of Irish constituencies that
better satisfied the criteria laid out by the Constitution.

## Background

Many representative democracies use electoral systems where a territory
is split into a number of small regions called electoral districts.
These can be considered the building blocks of *constituencies*, which
are specified regions that may elect a certain number of
representatives.

In these systems, the arrangement of constituencies can significantly
impact election results. Indeed, one can sufficiently manipulate the map
so as to favour a certain political party; this action is referred to as
*gerrymandering*. The word was first used in Boston in reaction to the
redrawing of constituencies through a bill signed by Elbridge Gerry,
which favoured the Democratic-Republican party. The redistricting was
said to resemble a mythological salamander, hence coining the term.

The problem of *redistricting* involves drawing a map of constituencies
such that all members of the population are fairly represented in the
electoral system. In this paper we focus on redistricting the
constituencies of Ireland, using an evolutionary algorithm devised to
optimise the configuration according to the objectives set out in the
Constitution of Ireland.

## Electoral Districting in Ireland

On 9 February 2023, a new state body called the Electoral Commission was
established to oversee elections in Ireland.
One of the key roles of the Electoral Commission is reviewing the the
Dáil Éireann constituencies, and making a report and recommendations in
relation to possible changes to constituency boundaries.

#### Basic Terminology {#basic-terminology .unnumbered}

-   The national parliament of Ireland is referred to as *Dáil Éireann*,
    or simply the Dáil.

-   An elected representative sitting in the Dáil is referred to as a
    *Teachta Dála* (TD).

-   Ireland is divided up into 3,440 regions known as *electoral
    divisions* (EDs).

-   These EDs are currently split between 39 *constituencies*. The
    current configuration of constituencies in Ireland is shown in
    Figure 1. The constituency
    boundaries can be changed by transferring EDs from one constituency
    to another. The number of constituencies is not fixed and may be
    altered in a redrawing of boundaries.

-   Ireland is also divided into 26 *counties*, which are administrative
    regions governed by bodies called county councils. The location of
    constituency boundaries is independent of the position of county
    boundaries, but it is considered desirable for constituencies to
    conform to county boundaries as far as is practicable. Larger
    counties are typically split into several constituencies, and some
    constituencies breach county boundaries to an appreciable extent, as
    illustrated in Figure 2.

![The current configuration of
constituencies.](images/current_configuration_numbered.png)
*Figure 1: The current configuration of constituencies.*

In this project, we define the redistricting problem to mean redrawing
the boundaries of constituencies such that criteria stipulated by the
Irish Constitution and the Electoral Commission are satisfied. These
requirements are explained below.

#### Constitutional Requirements

When deciding on any changes to the current constituency boundaries, the
Electoral Commission is required to observe the following provisions of
the Constitution:

-   Article 16.2.2° of the Constitution provides that:\
    *The number of members shall from time to time be fixed by law, but
    the total number of members of Dáil Éireann shall not be fixed at
    less than one member for each thirty thousand of the population, or
    at more than one member for each twenty thousand of the population.*

-   Article 16.2.3° of the Constitution provides that:\
    *The ratio between the number of members to be elected at any time
    for each constituency and the population of each constituency, as
    ascertained at the last preceding census, shall, so far as it is
    practicable, be the same throughout the country.*

![The current configuration of constituencies, overlaid with county
boundaries shown as grey
lines.](images/current_configuration.png)
*Figure 2: The current configuration of constituencies, overlaid with county boundaries shown as grey lines.*

#### Summary of Criteria

In determining the constituency boundaries of Ireland, the Electoral
Commission to satisfy the requirements just mentioned, as well as taking
several other criteria into account. The full set of criteria are the
following:

1.  Based on recent population figures, to satisfy Article 16.2.2of the
    Constitution, the total number of members of the Dáil shall not be
    less than 171 and not more than 181 (compared to 160 currently).

2.  Each constituency shall elect 3, 4 or 5 members.

3.  The breaching of county boundaries shall be avoided as far as it is
    practicable. (The extent to which this is satisfied by the current
    configuration is illustrated in Figure 2.)

4.  Each constituency shall be composed of contiguous
    areas.[]{#item:contiguity label="item:contiguity"}

5.  There shall be regard to geographic considerations including
    significant physical features and the extent of and the density of
    population in each constituency.

6.  Subject to the above matters, the Commission shall endeavour to
    maintain continuity in relation to the arrangement of
    constituencies.

Note that adherence to 4 is considered a priority, because it is a
'hard' requirement of the Constitution, and is designed to minimise
frustration amongst voters.

The large number of constraints imposed by the Constitution mean that
determining the optimal constituency boundaries is a challenging problem
in multi-objective optimisation. In this project, numerical methods were
implemented in order to find a solution which better satisfied the
requirements and recommendations set out above.

## Definitions and Nomenclature

In this section, the definitions of various terms and metrics used throughout the project are given.

#### National Ratio {#national-ratio .unnumbered}

The *National Ratio* of Ireland is defined as
$$
\text{National Ratio} = \frac{\text{Recorded Census Population}}{\text{Number of Dáil Seats}}.
$$
This metric represents the number of people each TD would represent in a
scenario with perfectly equal representation.

#### Seat Equivalent Representation {#seat-equivalent-representation .unnumbered}

The *Seat Equivalent Representation* (SER) of a constituency is defined
as 
$$
\text{SER} = \frac{\text{Population}}{\text{National Ratio}}.
$$ It quantifies the number of Dáil seats deserved by
a constituency based on its population size. To satisfy the requirements
of the Irish Constitution, constituency boundaries should be chosen such
that the SER of each constituency is very close to an integer between 3
and 5, so that the SER is very close to the actual number of seats
allocated to that constituency.

#### Variance from the National Average

In order to ensure equality of representation, the metric of *Variance
from the National Average* (VNA) is defined:
$$
\text{VNA} = \frac{\text{SER}-\text{Assigned Seats}}{\text{Assigned Seats}}.
$$
Positive and negative values correspond, respectively, to SER values
above and below the national average; ideally all constituencies would
have a VNA of zero. Past Constituency Commission reports have chosen a VNA of
$\pm5\%$ as an acceptable threshold value (the
Constituency Commission was responsible for recommending changes to
constituency boundaries before the establishment of the Electoral
Commission in 2023). In this project, we follow this choice and aim to
reduce the absolute value of the VNA of all constituencies to below $5\%$.

<center>
<em>Table 1: The current SER and VNA values of all 39 Irish constituencies.</em>

| Constituency         | Seats | SER   | VNA               |
|----------------------|-------|-------|-------------------|
| Carlow-Kilkenny      | 5     | 5.575 | **0.115**    |
| Cavan-Monaghan       | 5     | 5.048 | 0.010             |
| Clare                | 4     | 4.258 | **0.064**   |
| Cork East            | 4     | 4.075 | 0.019             |
| Cork North-Central   | 4     | 4.200 | 0.050             |
| Cork North-West      | 3     | 2.989 | -0.004          |
| Cork South-Central   | 4     | 4.090 | 0.023             |
| Cork South-West      | 3     | 2.826 | **-0.058** |
| Donegal              | 5     | 5.286 | 0.057             |
| Dublin Bay North     | 5     | 4.962 | -0.008          |
| Dublin Bay South     | 4     | 4.066 | 0.017             |
| Dublin Central       | 4     | 3.818 | -0.046          |
| Dublin Fingal        | 5     | 5.467 | **0.093**    |
| Dublin Mid-West      | 4     | 3.959 | -0.01           |
| Dublin North-West    | 3     | 2.423 | **-0.192** |
| Dublin Rathdown      | 3     | 3.170 | **0.057**   |
| Dublin South-Central | 4     | 4.103 | 0.026             |
| Dublin South-West    | 5     | 4.917 | -0.017          |
| Dublin West          | 4     | 4.182 | 0.046             |
| Dún Laoghaire        | 4     | 4.146 | 0.036             |
| Galway East          | 3     | 2.993 | -0.002          |
| Galway West          | 5     | 4.866 | -0.027          |
| Kerry                | 5     | 5.234 | 0.047             |
| Kildare North        | 4     | 4.523 | **0.131**    |
| Kildare South        | 4     | 4.212 | **0.053**    |
| Laois-Offaly         | 5     | 5.399 | **0.080**    |
| Limerick City        | 4     | 4.150 | 0.037             |
| Limerick County      | 3     | 3.037 | 0.012             |
| Longford-Westmeath   | 4     | 4.455 | **0.114**    |
| Louth                | 5     | 5.327 | **0.065**    |
| Mayo                 | 4     | 4.418 | **0.105**    |
| Meath East           | 3     | 3.320 | **0.107**    |
| Meath West           | 3     | 3.330 | **0.110**    |
| Roscommon-Galway     | 3     | 3.040 | 0.013             |
| Sligo-Leitrim        | 4     | 4.060 | 0.015             |
| Tipperary            | 5     | 5.405 | **0.081**    |
| Waterford            | 4     | 4.162 | 0.040             |
| Wexford              | 5     | 5.464 | **0.093**    |
| Wicklow              | 5     | 5.183 | 0.037             |

</center>

The current number of seats allocated to the 39 constituencies,
along with their SER and VNA values. VNA values that lie outside the acceptable threshold of $\pm0.05$ are shown in bold.

## Data Aggregation and Preparation

This project was written in Python. The library `pandas`
was used for handling data, `geopandas`
was used to implement geographic methods such as
unions and intersections, and to plot geographical data, and
`matplotlib` was used to render maps and plot graphs and
charts.

### Data Sources

The data used in the project came primarily from Tailte Éireann
(formerly Ordnance Survey Ireland). In particular, we used 2019 data on
electoral divisions, and 2017 data on
constituency boundaries. The operation of our
algorithm required us to know which constituency each ED belonged to,
and in fact this data was not included in the original datasets. We
instead had to find this manually, by using the `.representative_point`
method of `geopandas` to find a point inside each ED, and then using a
spatial join (`sjoin`) to merge the ED and constituency datasets
according to the constituency that contained each of these points. This
gave us a `GeoDataFrame` which linked EDs and constituencies, and
contained a `geometry` column which allowed the EDs to be plotted on a
map.

Since it was necessary to quantify the extent to which a configuration
breached county boundaries, we also needed geographical data on
counties. This was also obtained from a 2019 dataset made available by
Tailte Éireann. Finally, we also needed to know the
population of each ED. This data was obtained from the Central
Statistics Office. At the beginning of the project, only 2018 population
data was available, but data from the 2022 census became available in
August 2023, and it was this data that was
ultimately merged with the geographical data to find the final
dataframe. There was no population data for some EDs, so these were
assigned zero population.

An example of what was recorded in the dataframe for the ED
Bohernabreena is:

```python
    ED                                                BOHERNABREENA
    ED_ID                                                    267035
    GUID                       2ae19629-1ce0-13a3-e055-000000000001
    ESRI_OID                                                      8
    CON                                           DUBLIN SOUTH-WEST
    CON_ID                                                  260009C
    SEATS                                                         5
    POPULATION                                                 4496
    COUNTY                                                   DUBLIN
    PROVINCE                                               LEINSTER
    CENTROID_X                                            711258.06
    CENTROID_Y                                            720929.15
    AREA                                                43938821.49
    geometry      POLYGON ((708211.089 725425.627, 708215.62 725...
    NEIGHBOURS    [267006, 267159, 267143, 257046, 267083, 26714...
    NB_CONS                              [DUBLIN RATHDOWN, WICKLOW]
    BOUNDARY                                                      1
    CHANGE                                                        0
```

Some properties of each `ED` need explaining:

-   `CON` and `SEATS` detail the current constituency to which `ED`
    belongs, and the former's number of elected seats in the Dáil,

-   `ED_ID`, `GUID` and `ESRI_ID` are all different identification
    systems for Irish electoral divisions,

-   (`CENTROID_X`, `CENTROID_Y`), `geometry` and `AREA` contain
    information about the physical position, shape and area of `ED`
    respectively,

-   `NEIGHBOURS` keeps track of the ED IDs of of the electoral divisions
    with which `ED` shares a border, while `NB_CONS` is the list of
    `ED`'s neighbouring constituencies,

-   `BOUNDARY` is 1 if `ED` has a non-empty `NB_CONS` list or 0
    otherwise,

-   `CHANGE` is 1 if `ED` has previously been flipped as part of the
    evolution or 0 otherwise.

### Finding Neighbouring EDs

The arrays of neighbouring EDs and constituencies for each ED were
created by checking which shared a border using the
`geopandas.GeoSeries.touches` feature. This was streamlined by defining
a function `find_neighbours`, which is shown below. This function was applied to the original
ED dataset to obtain the `NEIGHBOURS` and `NB_CONS` columns of the
dataframe shown above. It was important that each element in these
columns was a `numpy` array rather than a Python list. We initially used
lists, but quickly encountered errors because lists are mutable and were
being incrementally altered in processes that were intended to be
independent.

```python
def find_neighbours(df):
        '''
        Finds the neighbours and neighbouring CONs of each ED
        '''
        # Create column containing empty neigbours list for each ED
        df['NEIGHBOURS'] = [[] for i in  range(len(df))]
        df['NB_CONS'] = [[] for i in  range(len(df))]
        df['BOUNDARY'] = [1 for i in  range(len(df))]
        df['CHANGE'] = [0 for i in  range(len(df))]
        
        # Find neighbours of each ED
        for i in range(len(df)):
            t = df['geometry'][i].touches(df['geometry'].values)
            # Create column of neighbouring EDs
            df.at[i,'NEIGHBOURS'] = df['ED_ID'][t].tolist()
            # Create column of neighbouring CONs        
            df.at[i,'NB_CONS'] = list(np.unique((df.loc[t,'CON']).tolist()))
            # Remove self from column
            if df.at[i,'CON'] in df.at[i,'NB_CONS']:
                df.at[i,'NB_CONS'].remove(df.at[i,'CON'])
            # Set type of ED
            if df.at[i,'NB_CONS'] == []:
                # No neighbouring CONs -> interior
                df.at[i,'BOUNDARY'] = 0
            df.at[i,'NEIGHBOURS'] = np.array(df.at[i,'NEIGHBOURS']).astype(str)
            df.at[i,'NB_CONS'] = np.array(df.at[i,'NB_CONS']) .astype(str)
        
    return df
```

It was then possible to identify which EDs had empty `NEIGHBOUR_CONS`
and their `BOUNDARY` value was changed from the initialised 1 to 0.

Once this function had been called on our aggregated dataframe, we had
all the information we needed to proceed with the development of our
algorithm.

## Outline

In this project, an evolutionary algorithm was implemented in Python in
order to optimise the constituency boundaries of Ireland with respect to
the criteria of the Constitution. In defining the algorithm, we
identified four main objectives based on our interpretation of the
Constitution:

1.  **Contiguity:** All constituencies should be composed of contiguous
    areas, except in the case of offshore islands (and other special
    cases discussed in Chapter 3.

2.  **SER:** Each constituency should have an SER which is close to an
    integer greater than or equal to 3. (If the SER of an existing
    constituency is found to be an integer greater than 5, then the
    constituency can in principle be split into several smaller
    constituencies with SERs close to 3, 4, or 5. For example, an
    existing constituency with an SER close to 6 could be split into two
    3-seater constituencies.)

3.  **County Boundaries:** The constituencies should respect county
    boundaries as much as possible.

4.  **Temporal Continuity:** The number of people living in EDs which
    have switched to different constituencies should be minimised as
    much as possible when attempting to satisfy the other three
    constraints.

Of these, the first two were considered 'primary objectives', and the
second two were considered 'secondary objectives'.

The candidate states were generated and optimised using an evolutionary
algorithm, which is discussed in Chapter 2. The four main
criteria above were used to define a reward function, which allowed the
configurations generated by the evolutionary algorithm at each
generation to be evaluated and filtered via a process akin to natural
selection. This is discussed in Chapter
3.
Finally, in Chapter 4, we discuss the results produced by the algorithm,
and possible improvements that could be made in future.