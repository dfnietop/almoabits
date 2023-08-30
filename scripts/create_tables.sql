create table if not exists public.control_cargue
(
    id        varchar                 not null
        constraint control_cargue_pk
            primary key,
    name      varchar                 not null,
    load_date timestamp default now() not null,
    process   boolean   default false not null
);

alter table public.control_cargue
    owner to fastapi;

create table if not exists public.dim_date
(
    id           varchar not null
        constraint dim_date_pk
            primary key,
    date         date    not null,
    day          varchar,
    day_week_num integer,
    day_num      integer,
    month_name   varchar,
    month_num    integer,
    quarter      integer,
    year         integer
);

alter table public.dim_date
    owner to fastapi;

create table if not exists public.dim_mccmnc
(
    id           varchar not null
        constraint dim_mccmnc_pk
            primary key,
    mcc          varchar,
    mnc          varchar,
    brand        varchar,
    operator     varchar,
    id_pais      varchar,
    load_date    timestamp,
    country_code varchar
);

alter table public.dim_mccmnc
    owner to fastapi;

create table if not exists public.dim_country
(
    id        varchar not null
        constraint dim_country_pk
            primary key,
    alpha_2   varchar,
    alpha_3   varchar,
    name      varchar,
    numeric   integer,
    load_date timestamp
);

alter table public.dim_country
    owner to fastapi;

create table if not exists public.fact_almoabits
(
    id            varchar not null
        constraint fact_almoabits_pk
            primary key,
    cdr_id        varchar not null,
    package_id    varchar not null,
    date_id       varchar not null
        constraint fact_almoabits_dim_date_id_fk
            references public.dim_date,
    mmc_mnc_id    varchar not null
        constraint fact_almoabits_dim_mccmnc_id_fk
            references public.dim_mccmnc,
    country_id    varchar not null
        constraint fact_almoabits_dim_country_id_fk
            references public.dim_country,
    imsi_id       varchar,
    imsi_no       varchar,
    inventory_id  varchar,
    iccid         varchar,
    type          varchar,
    connect_time  varchar,
    close_time    varchar,
    duration      double precision,
    direction     varchar,
    called_party  varchar,
    calling_party varchar,
    company_name  varchar
);

alter table public.fact_almoabits
    owner to fastapi;

