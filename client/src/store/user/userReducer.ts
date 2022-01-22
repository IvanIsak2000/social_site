import {ACCEPT_CHAT_NOTIFICATION, GET_USER_CHAT_NOTIFICATIONS, GET_USER_DATA} from './actionType';
import {GroupChatRequestI, UserI} from "../../interfaces";


interface UserReducerStateI {
    info: UserI | null,
    isAuth: boolean,
    chatRequestNotifications: Array<GroupChatRequestI>
}


const defaultState: UserReducerStateI = {
    info: null,
    isAuth: false,
    chatRequestNotifications: []
}

export const userReducer = (state = defaultState, action: any) => {
    switch (action.type) {
        case GET_USER_DATA:
            return {...state, ...action.payload}
        case GET_USER_CHAT_NOTIFICATIONS:
            return {...state, ...action.payload}
        case ACCEPT_CHAT_NOTIFICATION:
            const newRequestList = state.chatRequestNotifications.filter(request => request.id !== action.payload.acceptedRequest.id)
            return {...state, ...action.payload, chatRequestNotifications: newRequestList}
        default:
            return state
    }
}


