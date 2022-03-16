import React, {useState, useEffect, useRef} from 'react';
import { useSelector, useDispatch } from 'react-redux';

import Header from '../extend/Header';
import Error404NotFound from '../extend/Error404NotFound';
import SettingWindow from './include/setting/SettingWindow';
import {fetchGettingAllChatMembers, fetchGettingAllChatRequest} from "../../store/chat/actions";
import {GroupChatService} from "../../services/chatServices";


const ChatSettingPage = (props: any) => {
    const chatId = props.match.params.chatId;
    const dispatch = useDispatch()

    const currentUserData = useSelector((state: any) => state.user)
    const chatMembers = useSelector((state: any) => state.requestList.members)
    const chatRequests = useSelector((state: any) => state.requestList.requestList)

    const [chatData, setChatData] = useState({
        data: null,
        error: null
    })
    const service: any = useRef<GroupChatService>()

    useEffect(() => {
        service.current = new GroupChatService(chatId)
    }, [chatId])

    useEffect(() => {
        const fetchData = async() => {
            const response = service.current.getDetail()
            setChatData({data: response.data, error: response.status})
        }
        fetchData()
    }, [])

    useEffect(() => {
        dispatch(fetchGettingAllChatMembers(service.current))
        dispatch(fetchGettingAllChatRequest(service.current))
    }, [dispatch])


    if (currentUserData.isAuth && chatData.error !== 403) {
        return (
            <div>
                <Header/>
                <SettingWindow chatData={chatData} service={service.current}/>
            </div>
        )
    } else {
        return (
            <div>
                <Header/>
                <Error404NotFound/>
            </div>
        )
    }
}

export default ChatSettingPage;