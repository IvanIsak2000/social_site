import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux'
import axios from 'axios';

import FriendList from '../friend/FriendList';


interface friendsDataI {
    friends: Array<any>,
    error: number | null
}

const getFriends = async(userId: number) => {
    let data: friendsDataI = {
        friends: [],
        error: null
    }

    await axios.get("http://127.0.0.1:8000/api/v1/user/find/" + userId + "/friends/")
        .then((response) => {
            data.friends = response.data;
        })
        .catch((err) => {
            data.error = err.response.status;
        })

    return data;
}


const AddFriendTab = (props: any) => {
    const [friendsData, setFriendsData] = useState({
        list: [],
        error: null
    })
    const currentUserData = useSelector(state => state.user)


    useEffect(() => {
        getFriends(currentUserData.info.id)
            .then((result) => {
                setFriendsData({
                    list: result.friends,
                    error: result.error
                })
            })
    }, [])

    if (friendsData.list.length > 0 && !friendsData.error && currentUserData.info) {
        return (
            <div className="tab-pane fade" id="friend-tab" role="tabpanel" aria-labelledby="nav-home-tab">
                <FriendList friends={friendsData.list}/>
            </div>
        )
    } else {
        return (
            <div className="tab-pane fade" id="friend-tab" role="tabpanel" aria-labelledby="nav-home-tab">
                You don't have friends.
            </div>
        )
    }
}

export default AddFriendTab;