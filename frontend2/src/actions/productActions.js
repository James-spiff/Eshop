import { 
    PRODUCT_LIST_REQUEST, PRODUCT_LIST_SUCCESS, PRODUCT_LIST_FAIL,
    PRODUCT_DETAIL_REQUEST, PRODUCT_DETAIL_SUCCESS, PRODUCT_DETAIL_FAIL,
    PRODUCT_DELETE_REQUEST, PRODUCT_DELETE_SUCCESS, PRODUCT_DELETE_FAIL,
    PRODUCT_CREATE_REQUEST, PRODUCT_CREATE_SUCCESS, PRODUCT_CREATE_FAIL,
    PRODUCT_UPDATE_REQUEST, PRODUCT_UPDATE_SUCCESS, PRODUCT_UPDATE_FAIL,
    PRODUCT_CREATE_REVIEW_REQUEST, PRODUCT_CREATE_REVIEW_SUCCESS, PRODUCT_CREATE_REVIEW_FAIL,
    PRODUCT_TOP_REQUEST, PRODUCT_TOP_SUCCESS, PRODUCT_TOP_FAIL
} from '../constants/productConstants'
import axios from 'axios' //Used for connecting to an api

//redux thunk let's us make a function in another function in the case below " async = () => " comes after the 1st arrow function this gives us an async function within the initial function 
export const listProducts = (keyword = '') => async (dispatch) => {
    try{
        dispatch({ type: PRODUCT_LIST_REQUEST }) //this action fires the reducer which starts changing the state and then performs the action below
        
        //This get's the response from the api which will be passed to the next action
        const { data } = await axios.get(`/api/products/${keyword}`) //proxy: http://127.0.0.1:8000 set in package.json this let's us write a short form of the url without the 1st part of it
        //$keyword passes in a keyword at the end of the request by default it's empty but if the searchbox is used the value being searched is passed as the keyword

        //if the above action is successful it triggers the next action which changes the state and returns a payload from the api
        dispatch({
            type: PRODUCT_LIST_SUCCESS,
            payload: data
        })
    } catch ( error ) {
        //if the action fails this reducer is triggered and the state changes to the Failure state created in the reducer
        dispatch({
            type: PRODUCT_LIST_FAIL,
            payload: error.response && error.response.data.detail 
                ? error.response.data.detail 
                : error.message,    //an if statement using tenary operators that checks if an error message exists and returns it
        })
    }
}

export const listProductDetail = (id) => async (dispatch) => {
    try{
        dispatch({ type: PRODUCT_DETAIL_REQUEST }) //this action fires the reducer which starts changing the state and then performs the action below
        
        //This get's the response from the api which will be passed to the next action
        const { data } = await axios.get(`/api/products/${id}`) //proxy: http://127.0.0.1:8000 set in package.json this let's us write a short form of the url without the 1st part of it

        //if the above action is successful it triggers the next action which changes the state and returns a payload from the api
        dispatch({
            type: PRODUCT_DETAIL_SUCCESS,
            payload: data
        })
    } catch ( error ) {
        //if the action fails this reducer is triggered and the state changes to the Failure state created in the reducer
        dispatch({
            type: PRODUCT_DETAIL_FAIL,
            payload: error.response && error.response.data.detail 
                ? error.response.data.detail 
                : error.message,    //an if statement using tenary operators that checks if an error message exists and returns it
        })
    }
}



export const deleteProduct = (id) => async (dispatch, getState) => {
    try{
        dispatch({ type: PRODUCT_DELETE_REQUEST })  

        const { userLogin: { userInfo }, } = getState()

        const config = {
            headers: {
                'Content-type': 'application/json', 
                Authorization: `Bearer ${userInfo.token}`   
            }
        }

        const { data } = await axios.delete(`/api/products/delete/${id}`, config)
        
        dispatch({
            type: PRODUCT_DELETE_SUCCESS
        })
    } catch ( error ) {
        dispatch({
            type: PRODUCT_DELETE_FAIL,
            payload: error.response && error.response.data.detail 
                ? error.response.data.detail 
                : error.message,    
        })
    }
}


export const createProduct = () => async (dispatch, getState) => {
    try{
        dispatch({ type: PRODUCT_CREATE_REQUEST })  

        const { userLogin: { userInfo }, } = getState()

        const config = {
            headers: {
                'Content-type': 'application/json', 
                Authorization: `Bearer ${userInfo.token}`   
            }
        }

        const { data } = await axios.post(`/api/products/create/`, {}, config)
        
        dispatch({
            type: PRODUCT_CREATE_SUCCESS,
            payload: data,
        })
        
    } catch ( error ) {
        dispatch({
            type: PRODUCT_CREATE_FAIL,
            payload: error.response && error.response.data.detail 
                ? error.response.data.detail 
                : error.message,    
        })
    }
}


export const updateProduct = (product) => async (dispatch, getState) => {
    try{
        dispatch({ type: PRODUCT_UPDATE_REQUEST })  

        const { userLogin: { userInfo }, } = getState()

        const config = {
            headers: {
                'Content-type': 'application/json', 
                Authorization: `Bearer ${userInfo.token}`   
            }
        }

        const { data } = await axios.put(`/api/products/update/${product._id}/`, product, config)
        
        dispatch({
            type: PRODUCT_UPDATE_SUCCESS,
            payload: data,
        })

        dispatch({ 
            type: PRODUCT_DETAIL_SUCCESS,
            payload: data
        })
        
    } catch ( error ) {
        dispatch({
            type: PRODUCT_UPDATE_FAIL,
            payload: error.response && error.response.data.detail 
                ? error.response.data.detail 
                : error.message,    
        })
    }
}


export const reviewProduct = (productId, review) => async (dispatch, getState) => {
    try{
        dispatch({ type: PRODUCT_CREATE_REVIEW_REQUEST })  

        const { userLogin: { userInfo }, } = getState()

        const config = {
            headers: {
                'Content-type': 'application/json', 
                Authorization: `Bearer ${userInfo.token}`   
            }
        }

        const { data } = await axios.post(`/api/products/${productId}/reviews/`, review, config)
        
        dispatch({
            type: PRODUCT_CREATE_REVIEW_SUCCESS,
            payload: data,
        })
        
    } catch ( error ) {
        dispatch({
            type: PRODUCT_CREATE_REVIEW_FAIL,
            payload: error.response && error.response.data.detail 
                ? error.response.data.detail 
                : error.message,    
        })
    }
}


export const listTopProducts = () => async (dispatch) => {
    try{
        dispatch({ type: PRODUCT_TOP_REQUEST }) 
        
        
        const { data } = await axios.get(`/api/products/top/`) 

        dispatch({
            type: PRODUCT_TOP_SUCCESS,
            payload: data
        })
    } catch ( error ) {
       
        dispatch({
            type: PRODUCT_TOP_FAIL,
            payload: error.response && error.response.data.detail 
                ? error.response.data.detail 
                : error.message,   
        })
    }
}
