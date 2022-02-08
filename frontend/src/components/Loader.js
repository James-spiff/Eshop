import React from 'react'
import { Spinner } from 'react-bootstrap'

//This creates an animated spinner that will be used whenever the page is loading
function Loader() {
    return (
        <Spinner animation="border" role="status" style={{
            height: '100px',
            width: '100px', 
            margin: 'auto',
            display: 'block'
            }}
        >
            <span className='sr-only'>Loading...</span>

        </Spinner>
    )
}

export default Loader
