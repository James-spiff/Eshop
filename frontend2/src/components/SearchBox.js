import React, {useState} from 'react'
import { Button, Form } from 'react-bootstrap'
import { useHistory } from 'react-router-dom' //works like history but this functions in a component

function SearchBox() {

    const [keyword, setKeyword] = useState('')

    let history = useHistory()

    const submitHandler = (e) => {
        e.preventDefault()
        if (keyword) {
            history.push(`/?keyword=${keyword}&page=1`)    //Searches for the keyword entered by the user by passing it through the url. &page=1 starts the search from the 1st page to the last incase there are multiple pages
        } else {
            history.push(history.push(history.location.pathname))
        }
    }

    return (
        <Form onSubmit={submitHandler} inline>
            <Form.Control
                type='text'
                name='q'
                value={keyword}
                onChange={ (e) => setKeyword(e.target.value) }
                className='mr-sm 2 ml-sm-5'
            >

            </Form.Control>

            <Button
                type='submit'
                variant='outline-success'
                className='p-2'
            >
                Submit
            </Button>
            
        </Form>
    )
}

export default SearchBox
