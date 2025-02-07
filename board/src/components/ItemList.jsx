import { useEffect, useState } from "react";
import { getItemName } from "../common/utils";
import Person from "./types/Person";
import Tag from "./types/Tag";
import Place from "./types/Place";
import Location from "./types/Location";
import Group from "./types/Group";

const ItemList = ({api, reloadList}) => {

    const [items, setItems] = useState([]);

    useEffect(() => {
        refresh();
    }, [reloadList])

    const refresh = () => {
        fetch('/api/' + api + '/')
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                setItems(data)
            });
    }

    const getListContentComponent = (item) => {
        if (api === "people"){
            return <Person id={item.id} name={item.name} />
        }
        if (api === "tags"){
            return <Tag id={item.id} name={item.name} />
        }
        if (api === "places"){
            return <Place id={item.id} name={item.name} />
        }
        if (api === "groups"){
            return <Group id={item.id} name={item.name} />
        }
        if (api === "locations"){
            return <Location id={item.id} name={item.name} />
        }
    }

    return (
        <>
            <h2>{getItemName(api)} Listing<button onClick={refresh}>Refresh</button></h2>
            <ul>
                {items.map((item) => (
                    <li key={item.id}>{getListContentComponent(item)}</li>
                ))}
            </ul>
        </>
    );
};

export default ItemList;