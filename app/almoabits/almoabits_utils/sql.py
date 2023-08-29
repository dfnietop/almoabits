group_q_numbers_employess="""
select department,
       job,
       sum(q1) q1 ,
       sum(q2) q2,
       sum(q3) q3,
       sum(q4) q4
from vw_group_hired 
where vw_group_hired.year = :year
group by 1,2"""


total_numbers_employess_hired ='''
select 
    id,
    department, 
    year,
    hired
from vw_total_hired
where vw_total_hired.year = :year
'''


CARGUE_ARCHIVOS_SQL='''
SELECT *
FROM public.control_cargue a
where a.name = any(:file_list)
and a.process is FALSE
'''