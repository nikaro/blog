#!/usr/bin/python3

from email.utils import formataddr
import mailbox
from time import strftime

import pymysql.cursors


def main():
    dbconn = {
        'host': 'localhost',
        'read_default_file': '/root/.my.cnf',
        'db': 'wordpress',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
        }
    comments = get_comments_from_db(dbconn, exclude_types=('pingback', ))
    import_comments('wp_comments.mbox', comments)


def get_comments_from_db(dbconn: dict, exclude_types: tuple = ()) -> list:
    connection = pymysql.connect(**dbconn)
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT DISTINCT ' + \
                'wp_comments.comment_ID AS id, ' + \
                'wp_comments.comment_author AS author, ' + \
                'wp_comments.comment_author_email AS email, ' + \
                'wp_comments.comment_date AS date, ' + \
                'wp_comments.comment_content AS content, ' + \
                'wp_comments.comment_type AS type, ' + \
                'wp_comments.comment_parent AS parent, ' + \
                'wp_posts.post_title AS post ' + \
                'FROM wp_comments INNER JOIN wp_posts ' + \
                'WHERE wp_comments.comment_post_ID = wp_posts.ID ' + \
                ';'
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        connection.close()

    comments = [x for x in result if x['type'] not in exclude_types]

    return comments


def import_comments(mbox_path: str, comments: list):
    mbox = mailbox.mbox(mbox_path)
    mbox.lock()
    try:
        for comment in comments:
            # message data
            from_addr = comment['email'] or 'none'
            headers = {
                'from': formataddr((comment['author'], from_addr)),
                'to': '<~nka/public-inbox@lists.sr.ht>',
                'subject': 'Re: ' + comment['post'],
                'date': comment['date'].timetuple(),
                'id': '<' + str(comment['id']) + '@wp2mbox>',
                }
            if int(comment['parent']):
                headers['reply_to'] = '<' + str(comment['parent']) + '@wp2mbox>'
            text = comment['content'].encode()

            # format and add message
            msg = create_message(headers, text)
            mbox.add(msg)
            mbox.flush()
    finally:
        mbox.unlock()


def create_message(headers: dict, text: str) -> mailbox.mboxMessage:
    msg = mailbox.mboxMessage()
    msg['From'] = headers['from']
    msg['To'] = headers['to']
    msg['Subject'] = headers['subject']
    msg['Date'] = strftime('%a, %d %b %Y %H:%M:%S %z', headers['date'])
    msg['Message-Id'] = headers['id']
    if 'reply_to' in headers.keys():
        msg['In-Reply-To'] = headers['reply_to']
    msg.set_payload(text)

    return msg


if __name__ == '__main__':
    main()
