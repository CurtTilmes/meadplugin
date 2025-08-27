package rule

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/CurtTilmes/meadplugin/go/rule"
)

func init() {
	rule.Register("samplerule",
		evaluateSampleRule,
		"This is a sample rule.",
		`Long help for sample rule.
Call with makeanerror set to return an error.
Call with panic to cause a panic.
Call with skipthisone to skip this rule.
Call with retry to return a retry.
Call wtih failure to return failure.

Otherwise sets a couple of params and adds a few files.
`)
}

func evaluateSampleRule(_ context.Context, params rule.Params) (response *rule.Response, err error) {
	// If you do any long actions, check context for cancellation

	log.Printf("Evaluating samplerule")

	if e := params["makeanerror"]; e != "" {
		return nil, fmt.Errorf("some kind of error %q", e)
	}

	if params["panic"] != "" {
		panic("Panic is fine too, it gets caught")
	}

	if params["skipthisone"] != "" {
		return rule.Skip("why I'm skipping")
	}

	if params["retry"] != "" {
		return rule.Retry("Retry: " + time.Now().Add(time.Hour*2).Format(time.RFC3339))
	}

	if params["failure"] != "" {
		return rule.Failure("something isn't good")
	}

	r := rule.NewResponse()

	rule.Set(r, "ESDT", "MOD02HKM")
	rule.Set(r, "something", "whatever you want")

	rule.Add(r, "group/prefix/filename.hdf", &rule.Params{"ESDT": "someesdt"})
	rule.Add(r, "modaps-lads/MOD03/MOD03.blahblah.hdf", nil)

	return rule.Success(r)
}
