
const Place = ({id, name}) => {

    const getPlaceInfo = () => {
        fetch('/api/places/' + id)
            .then((response) => response.json())
            .then((data) => {
                // TODO draft dialog for displaying info
                console.log(data)
            });
    }


    return (
        <>
            <div onClick={getPlaceInfo}>({id}): {name}</div>
        </>
    );
};

export default Place;