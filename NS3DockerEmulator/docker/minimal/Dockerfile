############################################################
# Build stage
############################################################

FROM golang:1.9 as builder

# Building Beacon simple app
WORKDIR /var/log/golang
WORKDIR /go/src/github.com/chepeftw/Beacon

# RUN git clone https://github.com/chepeftw/Beacon.git
COPY ./Beacon /go/src/github.com/chepeftw/Beacon


WORKDIR /go/src/github.com/chepeftw/Beacon
RUN go get && CGO_ENABLED=0 go install -a -tags netgo -ldflags '-extldflags "-static"'

RUN ldd /go/bin/Beacon | grep -q "not a dynamic executable"


############################################################
# Run stage
############################################################

FROM alpine

#RUN apk update && apk add bash
RUN apk add tshark bash

COPY wrapper.sh /wrapper.sh
RUN chmod +x /wrapper.sh
COPY --from=builder /go/bin/Beacon /beacon

#RUN tshark -r /var/log/golang/capture.cap
#RUN tshark -b filesize:100 -a files:20 -w /var/log/golang/temp.pcap -q &

#CMD ["bash", "/wrapper.sh"]
CMD /wrapper.sh

# docker build -t hello-world-multi-stage .
# docker run hello-world-multi-stage
# docker image ls hello-world-multi-stage