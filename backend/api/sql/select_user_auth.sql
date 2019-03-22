-- В метод передаются Логин и пароль, возвращается id_user
insert into "session"("session", "id_user")
select md5(random()::text || clock_timestamp()::text)::text
, "id_user"
from (
  select "id_user"
  from "users"
  where "login" = '{login}'
    and "password" = '{password}'
  limit 1
) nd
where "id_user" is not null
returning "session" as "session"