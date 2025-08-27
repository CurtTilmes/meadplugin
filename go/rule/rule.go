package rule

import (
	"context"
	"fmt"
	"log"
	"maps"
	"strconv"

	"github.com/CurtTilmes/meadplugin"
)

// Aliases for simplicity
type Response = meadplugin.EvaluateResponse
type Item = meadplugin.Item
type Params = map[string]string

// Signature for the Evaluation Function for each rule
type EvaluationFunction = func(ctx context.Context, params Params) (*Response, error)

type Rule struct {
	Name      string
	EvalFunc  EvaluationFunction
	ShortHelp string
	LongHelp  string
}

var RuleTable map[string]Rule = map[string]Rule{}

func Register(rule string, evalfunc EvaluationFunction, shorthelp string, longhelp string) {
	log.Printf("Register %q", rule)

	RuleTable[rule] = Rule{
		Name:      rule,
		EvalFunc:  evalfunc,
		ShortHelp: shorthelp,
		LongHelp:  longhelp,
	}
}

func ParamInt(params Params, key string) (val int, err error) {
	str, ok := params[key]
	if !ok {
		return 0, fmt.Errorf("%s not found", key)
	}

	return strconv.Atoi(str)
}

// Make a new response
func NewResponse() *Response {
	return &Response{Params: Params{}, Items: []*Item{}}
}

// Set a param to a value
func Set(r *Response, key string, val string) {
	r.Params[key] = val
}

// Add an item identifier (and metadata) to the return list
func Add(r *Response, id string, metadata *Params) {
	f := meadplugin.Item{
		Id: id,
	}
	if metadata != nil {
		f.Metadata = make(Params)
		maps.Copy(f.Metadata, *metadata)
	}
	r.Items = append(r.Items, &f)
}

// set Status to Success
func Success(r *Response) (*Response, error) {
	r.Status = meadplugin.RuleStatus_RULE_STATUS_SUCCESS
	return r, nil
}

// set Status to Skip
func Skip(message string) (*Response, error) {
	return &Response{
		Status:  meadplugin.RuleStatus_RULE_STATUS_SKIP,
		Message: message,
	}, nil
}

// set Status to Retry and store the timestamp
func Retry(message string) (*Response, error) {
	return &Response{
		Status:  meadplugin.RuleStatus_RULE_STATUS_RETRY,
		Message: message,
	}, nil
}

func Failure(message string) (*Response, error) {
	return &Response{
		Status:  meadplugin.RuleStatus_RULE_STATUS_FAILURE,
		Message: message,
	}, nil
}
