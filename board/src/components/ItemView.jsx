import { useEffect, useState } from "react";
import ItemList from "./ItemList";
import { getItemName } from "../common/utils";
import { RuxButton, RuxSelect, RuxOption, RuxInput } from "@astrouxds/react";

const ItemView = ({api}) => {

    const [name, setName] = useState('');
    const [triggerList, setTriggerList] = useState(false);
    const [types, setTypes] = useState([])
    const [selectedType, setSelectedType] = useState('');


    useEffect(() => {
        if (api === "locations" || api === "groups"){
            console.log("fetching types")
            fetch('/api/' + api + '/types')
                .then((response) => response.json())
                .then((data) => {
                    setTypes(data)
                    setSelectedType(data[0])
                    console.log(data)
                });
        }}, [])


    const makePayload = () => {
        if (api === "locations" || api === "groups"){
            return { name: name, type: selectedType }
        }
        return { name: name }
    }


    const create = async() => {
        console.log("trying to create something")
        console.log("Name: " + name)
        console.log("Type: " + selectedType)

        if (name !== ""){
            const response = await fetch('/api/' + api + '/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(makePayload())
            });

            if (response.status === 201) {
                setName('');
                setTriggerList(prev => !prev);
            }
            else if (response.status === 409){
                alert(getItemName(api) + ' Already Exists')
            }
            else {
                alert('Error Creating ' + getItemName(api));
            }
        }
    };

    return (
        <div>
            <h1>{getItemName(api)} Management</h1>

            <h2>Create a {getItemName(api)}</h2>
            <RuxInput label={"Create " + getItemName(api)} type="text" placeholder={getItemName(api) + " Name"} value={name} onRuxinput={ (e) => {setName(e.target.value)}}></RuxInput>

            {api === "locations" || api === "groups" ? (
                <RuxSelect label={`Select ${getItemName(api)} Type`} onRuxchange={(e) => {setSelectedType(e.target.value)}} >
                    {types.map((item_type) => (
                        <RuxOption key={item_type} label={item_type} value={item_type} />
                        )
                    )}
                </RuxSelect>
            ) : null}

            <RuxButton onClick={create}>Create {getItemName(api)}</RuxButton>

            <br />

            <ItemList api={api} reloadList={triggerList} />

        </div>
    );
};

export default ItemView;