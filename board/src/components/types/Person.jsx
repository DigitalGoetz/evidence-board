import { RuxButton, RuxSelect, RuxOption, RuxInput, RuxDialog } from "@astrouxds/react";
import { useState } from "react";

const Person = ({id, name}) => {

    const [dialogOpen, setDialogOpen] = useState(false);
    const [personData, setPersonData] = useState(null);

    const getPersonInfo = () => {
        fetch('/api/people/' + id)
            .then((response) => response.json())
            .then((data) => {
                // TODO draft dialog for displaying info
                console.log(data)
                setPersonData(data);
                setDialogOpen(true);
            });
    }

    return (
        <>
            <div onClick={getPersonInfo}>({id}): {name}</div>

            <RuxDialog 
                open={dialogOpen}
                onRuxdialogclosed={() => setDialogOpen(false)}>
                <div slot="header">Person Details</div>
                <div>
                    {personData && (
                        <div>
                            <p>ID: {personData.id}</p>
                            <p>Name: {personData.name}</p>
                        </div>
                    )}
                </div>
                <div slot="footer">
                    <RuxButton 
                        secondary 
                        onClick={() => setDialogOpen(false)}
                    >
                        Close
                    </RuxButton>
                </div>
            </RuxDialog>
        </>
    );
};

export default Person;