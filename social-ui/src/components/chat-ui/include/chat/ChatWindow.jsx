import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { v4 as uuidv4 } from 'uuid';

import ChatList from './ChatList';


const ChatWindow = (props) => {
    return (
        <div className="container">
            <div className="card">
                <div className="row">
                    <div className="col-11 col-md-10 col-lg-9 col-xl-9 mx-auto" style={{display: "flex"}}>
                        <input type="text" className="form-control my-3 ml-2" placeholder="Search..."/>
                        <button className="btn btn-primary my-3 ml-2">Найти</button>
                    </div>
                </div>
                <hr/>
                <div className="row">
                    <div className="col-12">
                        <ChatList chats={props.groupChats} type_is_group={true} userData={props.userData}/>
                    </div>
                </div>
                {"\n"}
                <div className="row">
                    <div className="col-12">
                        <ChatList chats={props.personalChats} type_is_group={false} userData={props.userData}/>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ChatWindow;