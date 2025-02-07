

const getItemName = (api) => {
    switch (api) {
        case 'people':
            return 'People';
        case 'tags':
            return 'Tag';
        case 'groups':
            return 'Group';
        case 'places':
            return 'Place';
        case 'locations':
            return 'Location';
    }
}




export {getItemName};