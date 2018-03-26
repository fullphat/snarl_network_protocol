/*

BeSnarlNotify -- a Snarl notification client for BeOS and Haiku
Copyright (c) 2018 full phat products

IMPORTANT NOTE: I do not profess to be a c coder.  Indeed, the last time 
I touched C was in 1992 at University.  Suggestions for improvements 
or - indeed - complete re-writes are welcomed.

Please see the Wiki page (here) for usage instructions and other useful 
information.

To do:

-i: notification id
-s: sticky
-y: priority (-2, -1, 0, 1, 2)
Events

*/

#include<stdio.h>
#include<string.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netdb.h>
#include<arpa/inet.h>

#define BOLD "\033[1m"
#define RESET "\033[0m"

#define VERSION "1.0"
#define DEFAULT_PASSWORD "do_not_steal_this"

int snp31send(char* host, int port, char *data);
void out(char* text);
void outn(char* text);
void outb(char* text);

int verbose = 0;
int quiet = 0;
int doNotRegister = 0;
int debug = 0;
 
int main(int argc , char *argv[])
{
    int r;
    int i;

    char portstr[6]="";
    char appId[100]="", appTitle[100]="", pass[100]="";
    char title[100]="", body[100]="", icon[100]="", callback[128]="";

    char host[100]="";
    int port = 9888;
    char *ptr;

    char msg[2000]="";

    if (argc < 2)
    {
        puts("\nUsage: BeSnarlNotify [-t title] text\n\n");
        return 0;
    }

    // start processing args...

    for (i = 0; i < argc; i++)
    {
        //printf("argc: %d '%s'\n", i, argv[i]);
        if (strcmp(argv[i], "-t") == 0)
        {
            // title
            i++;
            if (i < argc)
                strlcpy(title, argv[i], strlen(title)-1);
        }
        else if (strcmp(argv[i], "-b") == 0)
        {
            // body
            i++;
            if (i < argc)
                strlcpy(body, argv[i], strlen(body)-1);
        }
        else if (strcmp(argv[i], "-i") == 0)
        {
            // icon
            i++;
            if (i < argc)
                strlcpy(icon, argv[i], strlen(icon)-1);
        }
        else if (strcmp(argv[i], "-h") == 0)
        {
            // host
            i++;
            if (i < argc)
                strlcpy(host, argv[i], strlen(host)-1);
        }
        else if (strcmp(argv[i], "-p") == 0)
        {
            // port
            i++;
            if (i < argc)
                strlcpy(portstr, argv[i], strlen(portstr)-1);
        }
        else if (strcmp(argv[i], "-a") == 0)
        {
            // appId
            i++;
            if (i < argc)
                strlcpy(appId, argv[i], strlen(appId)-1);
        }
        else if (strcmp(argv[i], "-l") == 0)
        {
            // callback
            i++;
            if (i < argc)
                strlcpy(callback, argv[i], strlen(callback)-1);
        }
        else if (strcmp(argv[i], "-w") == 0)
        {
            // password
            i++;
            if (i < argc)
                strlcpy(pass, argv[i], strlen(pass)-1);
        }
        else if (strcmp(argv[i], "--v") == 0 || strcmp(argv[i], "--verbose") == 0)
        {
            verbose = 1;
        }
        else if (strcmp(argv[i], "--q") == 0 || strcmp(argv[i], "--quiet") == 0)
        {
            quiet = 1;
        }
        else if (strcmp(argv[i], "--noreg") == 0)
        {
            doNotRegister = 1;
        }
        else if (strcmp(argv[i], "--debug") == 0)
        {
            debug = 1;
        }
    }


    // welcome text...

    outb("\nBeSnarlNotify " VERSION);

    // host...

    if (host[0] == '\0')
        strlcpy(host, "127.0.0.1", strlen(host)-1);

    // port...

    if (portstr[0] != '\0')
    {
        port = strtol(portstr, &ptr, 0);
        if (port == 0)
        {
            puts(BOLD "Failed: bad port" RESET);
            return 1;
        }
    }

    // register...

    if (doNotRegister == 0)
    {
        outn("(Register)");
        strcpy(msg, "SNP/3.1 REGISTER\r\n");
        strcat(msg, "app-id: ");
        if (appId[0] != '\0')
        {
            // custom app identifier...
            strcat(msg, appId);
        }
        else
        {
            strcat(msg, "net.fullphat.BeSnarlNotify");
        }
        strcat(msg, "\r\n");

        strcat(msg, "title: ");
        if (appTitle[0] != '\0' && appId[0] != '\0')
        {
            // custom title (only if custom app id specified)
            strcat(msg, appTitle);
        }
        else
        {
            strcat(msg, "BeSnarlNotify");
        }
        strcat(msg, "\r\n");

        // password

        strcat(msg, "password: ");
        if (pass[0] != '\0')
        {
            strcat(msg, pass);
        }
        else
        {
            strcat(msg, DEFAULT_PASSWORD);
        }
        strcat(msg, "\r\n");



        strcat(msg, "END\r\n");
        r = snp31send(host, port, msg);
        if (r != 0)
            return r;
    }

    // notify...

    outn("(Notify)");
    strcpy(msg, "SNP/3.1 NOTIFY\r\n");

    // appId: if one provided, use it, otherwise use ours...
    strcat(msg, "app-id: ");
    if (appId[0] != '\0')
    {
        strcat(msg, appId);
    }
    else
    {
        strcat(msg, "net.fullphat.BeSnarlNotify");
    }
    strcat(msg, "\r\n");

    if (title[0] != '\0')
    {
        strcat(msg, "title: ");
        strcat(msg, title);
        strcat(msg, "\r\n");
    }

    if (body[0] != '\0')
    {
        strcat(msg, "text: ");
        strcat(msg, body);
        strcat(msg, "\r\n");
    }

    if (icon[0] != '\0')
    {
        strcat(msg, "icon: ");
        strcat(msg, icon);
        strcat(msg, "\r\n");
    }

    if (callback[0] != '\0')
    {
        strcat(msg, "callback: ");
        strcat(msg, callback);
        strcat(msg, "\r\n");
    }

    // password

    strcat(msg, "password: ");
    if (pass[0] != '\0')
    {
        strcat(msg, pass);
    }
    else
    {
        strcat(msg, DEFAULT_PASSWORD);
    }
    strcat(msg, "\r\n");


    strcat(msg, "END\r\n");
    r = snp31send(host, port, msg);

    outn("");

    return r;

}

/*

snp31send -- simple SNP 3.1 send/receive helper

Inputs
------
host - name or IP address of host to send to
port - port to send to
data - data to send

Return Value
------------

Returns 0 (SNARL_SUCCES) if ok, or Snarl error number otherwise

IMPORTANT: Only returns an error if _sending_ the data failed
(e.g. couldn't connect to remote computer).  At the moment this
function does not parse the return message from Snarl.

*/

int snp31send(char *host, int port, char *data)
{
    int sock;
    struct sockaddr_in server;
    char message[2048]="", server_reply[4096]="";
    char p[100] = "";

    // create socket...

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1)
    {
        printf("Could not create socket");
    }

    server.sin_addr.s_addr = inet_addr(host);
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
 
    // connect...

    out("Connecting to ");
    out(host);
    out(":");
    sprintf(p, "%d", port);
    out(p);
    out("...");
    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0)
    {
        outn("failed");
        return 123;        // ERROR_CONNECTION_FAILED
    }
    outn("done");

    if (debug)
    {
        // print out the packet we're going to send...
        outn(BOLD);
        outn(data);
        outn(RESET);
    }

    out("Sending...");
    strcpy(message, data);
    if(send(sock, message, strlen(message), 0) < 0)
    {
        outn("failed");
        return 123;        // ERROR_CONNECTION_FAILED
    }
    outn("done");

    out("Wating for reply...");
    if (recv(sock, server_reply, strlen(server_reply)-1, 0) < 0)
    {
        outn("failed");
        return 123;        // ERROR_CONNECTION_FAILED
    }
    outn("done");

    if (verbose)
    {
        out(BOLD);
        out(server_reply);
        out(RESET);
    }
 
    close(sock);
    return 0;
}

void out(char *text)
{
    if (quiet == 0)
        printf(text);
}

void outn(char *text)
{
    if (quiet == 0)
        puts(text);
}

void outb(char *text)
{
    if (quiet == 0)
    {
        printf(BOLD);
        puts(text);
        printf(RESET);
    }
}
