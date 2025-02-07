
const Group = ({id, name}) => {

    const getGroupInfo = () => {
        fetch('/api/groups/' + id)
            .then((response) => response.json())
            .then((data) => {
                // TODO draft dialog for displaying info
                console.log(data)
            });
    }


    return (
        <>
            <div onClick={getGroupInfo}>({id}): {name}</div>
        </>
    );
};

export default Group;