package main

import (
	"encoding/json"
	"log"
	"io/ioutil"
	"net/http"
)

func main() {
	// Gives the list of calendars by date.

	path := "http://legislation.nysenate.gov/api/3/calendars/2016?key=zD19K0cX8fPnd8pAayNA7m50DAq4XbkA"

	resp, err := http.Get(path)
	if err != nil {
		log.Printf("error %v accessing path %+v", err, path)
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Printf("error %v accessing path %+v", err, path)
	}
    

	var cal map[string]interface{}
	err = json.Unmarshal(body, &cal)
	if err != nil {
		log.Printf("Error parsing json %v", err)
	} // Store previous calendar number
	success := cal["success"]
	if success != true {
		log.Printf("Error retrieving calendars")
	}
	result := cal["result"]
	log.Printf("result is %v", result)
}
