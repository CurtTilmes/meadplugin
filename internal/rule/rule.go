package rule

import (
	"context"
	"fmt"
	"log"
	"regexp"
	"time"

	pb "github.com/CurtTilmes/meadplugin/internal/pb"
	"google.golang.org/protobuf/types/known/timestamppb"
)

type Response = pb.EvaluateResponse

type EvaluationFunction = func(ctx context.Context, params map[string]string) (*Response, error)

type Rule struct {
	Name       string
	Version    string
	RuleParams map[string]string
	JobParams  []string
	Evaluate   EvaluationFunction
}

var ruleTable map[string]*Rule = map[string]*Rule{}

func Register(rule *Rule) {
	r := regexp.MustCompile(`^\d+\.\d+\.\d+-\d+$`)
	if !r.MatchString(rule.Version) {
		log.Fatalf("Bad Rule Version for %q - %q", rule.Name, rule.Version)
	}
	ruleTable[rule.Name] = rule
}

func IdentifyRules() (rules []*pb.Rule) {

	for _, r := range ruleTable {
		rules = append(rules, &pb.Rule{
			Name:       r.Name,
			Version:    r.Version,
			RuleParams: r.RuleParams,
			JobParams:  r.JobParams})
	}
	return rules
}

func Evaluate(ctx context.Context, in *pb.EvaluateRequest) (res *pb.EvaluateResponse, err error) {
	name := in.GetRuleName()
	params := in.GetParams()

	rule, ok := ruleTable[name]
	if !ok {
		return nil, fmt.Errorf("Unknown rule %q", name)
	}

	defer func() {
		if r := recover(); r != nil {
			log.Printf("Evaluate Crashed, Recovering")
			err = fmt.Errorf("Evaluate Crashed, rule %q", name)
		}
	}()

	return rule.Evaluate(ctx, params)
}

func NewResponse() *Response {
	return &Response{}
}

func Set(r *Response, key string, val string) {
	if r.JobParams == nil {
		r.JobParams = map[string]string{key: val}
		return
	}
	r.JobParams[key] = val
}

func Add(r *Response, fileid string) {
	if r.Files == nil {
		r.Files = []string{fileid}
		return
	}
	r.Files = append(r.Files, fileid)
}

func Success(r *Response) (*Response, error) {
	r.Status = pb.RuleStatus_RULE_STATUS_SUCCESS
	return r, nil
}

func Skip(r *Response) (*Response, error) {
	r.Status = pb.RuleStatus_RULE_STATUS_SKIP
	return r, nil
}

func Retry(r *Response, t time.Time) (*Response, error) {
	r.RetryTime = timestamppb.New(t)
	r.Status = pb.RuleStatus_RULE_STATUS_RETRY
	return r, nil
}
