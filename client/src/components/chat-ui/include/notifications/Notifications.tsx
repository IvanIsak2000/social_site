export const GroupChatNotification = () => {
    return (
        <div className="alert alert-primary" role="alert">
            Список чатов на этой странице отсортирован по их названию. Последние сообщения не обновляются в реальном времени.
            {'\n'}<a href="/chats/" className="alert-link"> Перейти в общий список чатов</a>.
        </div>
    )
}