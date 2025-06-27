package rule

import (
	"context"
	"fmt"
	"time"

	pb "github.com/CurtTilmes/meadplugin/internal/pb"
)

func init() {
	Register(&Rule{
		Name:       "samplerule",
		Version:    "1.2.3-4",
		RuleParams: map[string]string{"some-param": "some-value"},
		JobParams:  []string{"another-param"},
		Evaluate:   evaluate,
	})
}

func evaluate(_ context.Context, params map[string]string) (response *pb.EvaluateResponse, err error) {
	r := NewResponse()

	if e := params["makeanerror"]; e != "" {
		return nil, fmt.Errorf("some kind of error %q", e)
	}

	if params["skipthisone"] != "" {
		return Skip(r)
	}

	if params["retry"] != "" {
		return Retry(r, time.Now().Add(time.Hour*2)) // try again in 2 hours
	}

	Set(r, "ESDT", "MOD02HKM")
	Set(r, "something", "whatever you want")

	Add(r, "group/prefix/filename.hdf")
	Add(r, "modaps-lads/MOD03/MOD03.blahblah.hdf")
	return Success(r)
}
