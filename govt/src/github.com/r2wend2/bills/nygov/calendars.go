package ny

import(
"time"
)

type Calendars struct {
	success      bool   `json:"success"`
	message      string `json:"message"`
	responseType []string `json:"responseType"`
	total        int    `json:"total"`
	offsetStart  int    `json:"offsetStart"`
	offsetEnd    int    `json:"offsetEnd"`
	limit        int    `json:"limit"`
	r           Result   `json:"result"`
}
type Result struct {
	items []Item `json:"items"`
	size int `json:"size"`
}

type Item struct {
	year  int `json:"year"`
	calno int `json:"calendarNumber"`
	fc    Caltype `json:"floorCalendar"`
	sc    Caltype `json:"supplementalCalendars"`
	al    Caltype `json:"activeLists"`
	date  time.Time `json:"calDate"`
}

type Caltype struct {
	year         int       `json:"year"`
	calno        int       `json:"calendarNumber"`
	version      string    `json:"version"`
	date         time.Time `json:"calDate"`
	release      time.Time `json:"releaseDateTime"`
	totalEntries int       `json:"totalEntries"`
}
