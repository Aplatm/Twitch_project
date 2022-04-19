create table `2020_stats`
(
    `Rank`               int          null,
    Channel              varchar(255) not null
        primary key,
    `Watch Time (Hours)` int          null,
    `Stream Time(Hours)` int          null,
    `Peak viewers`       int          null,
    `Average viewers`    int          null,
    Followers            int          null,
    `Followers gained`   int          null,
    `Views gained`       int          null,
    Partnered            tinyint(1)   null,
    Mature               tinyint(1)   null,
    Language             text         null
);

create table `2022_stats`
(
    `Rank`               int          null,
    Channel              varchar(255) not null
        primary key,
    `Watch Time (Hours)` int          null,
    `Stream Time(Hours)` int          null,
    `Peak Views`         int          null,
    `Average Viewers`    int          null,
    Followers            int          null,
    `Followers gained`   int          null,
    `Views gained`       int          null,
    Partnered            text         null,
    Mature               text         null,
    Language             text         null
);


