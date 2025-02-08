


const PersonInfo = ({id, name}) => {

    const getPersonInfo = () => {
        fetch('/api/people/' + id)
            .then((response) => response.json())
            .then((data) => {
                // TODO draft dialog for displaying info
                console.log(data)
            });
    }


    return (
        <>
            <div onClick={getPersonInfo}>({id}): {name}</div>
        </>
    );
};

export default PersonInfo;