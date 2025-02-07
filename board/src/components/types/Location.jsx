
const Location = ({id, name}) => {

    const getLocationInfo = () => {
        fetch('/api/locations/' + id)
            .then((response) => response.json())
            .then((data) => {
                // TODO draft dialog for displaying info
                console.log(data)
            });
    }


    return (
        <>
            <div onClick={getLocationInfo}>({id}): {name}</div>
        </>
    );
};

export default Location;