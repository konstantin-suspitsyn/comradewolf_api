from comradewolf.universe.olap_structure_generator import OlapStructureGenerator
from fastapi import Depends

from backend.api.pydantic.model_olap import OlapUser, OlapTableResponse, OlapToml, OlapUserFromToken
from backend.core_structure import CoreContainer, OlapDbSettings
from backend.db.database import database
from backend.db.user_service import get_current_active_user

sql_permitted_olap_tables = """
    select 
        ot."name", ot.id
    from cwb.user_pesmission up 
    inner join cwb.olap_table ot 
        on up.olap_id = ot.id 
    where up.id = {};
"""

sql_is_table_in_user = """
    SELECT count(up.id) as "count_tables"
FROM cwb.user_permission up
inner join cwb.olap_table ot
	on ot.id = up.olap_id 
where up.user_id = {}
and ot."name" = '{}';

"""

sql_one_toml = """
    select
         id 
        ,"name"
        ,link_toml 
    from cwb.olap_table ot 
    where ot."name" = '{}'
"""

sql_olap_info = """
    SELECT 
         oc.id
        ,oc.host
        ,oc.host_type
        ,oc.port
        ,oc.port_type
        ,oc.username
        ,oc.username_type
        ,oc."password"
        ,oc.password_type
        ,oc."database"
        ,oc.database_type
        ,dt."name" as database_name
        ,oc.olap_id
        ,oc.additional
        ,oc."comment"
        ,oc.created_at
        ,oc.updated_at
        ,oc.max_connections
    FROM cwb.olap_connection oc
    inner join cwb.database_type dt 
        on dt.id = oc.database_type 
    where 
        oc.olap_id = {};
    """


async def get_list_of_olap_tables(current_user: OlapUserFromToken = Depends(get_current_active_user)) -> list[OlapTableResponse]:
    olap_tables = list()

    all_tables = await database.fetch_all(sql_permitted_olap_tables.format(current_user.id))

    for table in all_tables:
        olap_tables.append(OlapTableResponse(id=table["id"], name=table["name"]))

    return olap_tables


async def get_frontend_fields(olap_table_name: str, current_user: OlapUserFromToken = Depends(get_current_active_user)):
    is_table_allowed = await database.fetch_one(sql_is_table_in_user.format(current_user.id, olap_table_name))

    if is_table_allowed["count_tables"] == 0:
        # TODO: Throw an error
        print("throw an error")

    frontend_fields = await get_toml_info(olap_table_name)

    return frontend_fields


async def get_toml_info(olap_name: str):
    """
    Returns info about olap table
    :param olap_name: name of olap table. Unique in database
    :return:
    """
    result = await database.fetch_one(sql_one_toml.format(olap_name))

    olap_name_toml = OlapToml(id=result["id"], name=result["name"], link_toml=result["link_toml"])

    all_olap = CoreContainer()

    if olap_name_toml.name not in all_olap:
        olap_info = await database.fetch_one(sql_olap_info.format(olap_name_toml.id))

        olap_structure = OlapStructureGenerator(olap_name_toml.link_toml)

        olap_db_settings = OlapDbSettings(olap_info["host"],
                                          str(olap_info["port"]),
                                          olap_info["database"],
                                          olap_info["username"],
                                          olap_info["password"],
                                          olap_info["database_type"],
                                          olap_info["max_connections"],
                                          olap_structure.get_front_fields())

        all_olap.create_olap_structure(olap_name_toml.name, olap_db_settings)

    return {"olap_table_name": olap_name_toml.name, "fields": all_olap.get_front_fields(olap_name_toml.name)}
