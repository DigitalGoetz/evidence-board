
const Item = ({id, name, api}) => {

    const getInfo = () => {
        fetch('/api/' + api + '/' + id)
            .then((response) => response.json())
            .then((data) => {
                // TODO draft dialog for displaying info
                console.log(data)
            });
    }


    return (
        <>
            <div onClick={getInfo}>({id}): {name}</div>
        </>
    );
};

export default Item;