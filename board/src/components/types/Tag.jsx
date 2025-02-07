
const Tag = ({id, name}) => {

    const getTagInfo = () => {
        fetch('/api/tags/' + id)
            .then((response) => response.json())
            .then((data) => {
                // TODO draft dialog for displaying info
                console.log(data)
            });
    }


    return (
        <>
            <div onClick={getTagInfo}>({id}): {name}</div>
        </>
    );
};

export default Tag;