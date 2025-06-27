package rule

import (
	"context"
	"fmt"
	"time"

	pb "github.com/CurtTilmes/meadplugin/internal/pb"
	"google.golang.org/protobuf/types/known/timestamppb"
)

type EvaluationFunction = func(ctx context.Context, params map[string]string) (*pb.EvaluateResponse, error)

type Rule struct {
	Name       string
	Version    string
	RuleParams map[string]string
	JobParams  []string
	Evaluate   EvaluationFunction
}

var ruleTable map[string]*Rule = map[string]*Rule{}

func Register(rule *Rule) {
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

func Evaluate(ctx context.Context, in *pb.EvaluateRequest) (*pb.EvaluateResponse, error) {
	r := in.GetRuleName()
	params := in.GetParams()

	rule, ok := ruleTable[r]
	if !ok {
		return nil, fmt.Errorf("Unknown rule %q", r)
	}
	return rule.Evaluate(ctx, params)
}

func NewResponse() *pb.EvaluateResponse {
	return &pb.EvaluateResponse{}
}

func Set(r *pb.EvaluateResponse, key string, val string) {
	if r.JobParams == nil {
		r.JobParams = map[string]string{key: val}
		return
	}
	r.JobParams[key] = val
}

func Add(r *pb.EvaluateResponse, fileid string) {
	if r.Files == nil {
		r.Files = []string{fileid}
		return
	}
	r.Files = append(r.Files, fileid)
}

func Success(r *pb.EvaluateResponse) (*pb.EvaluateResponse, error) {
	r.Status = pb.RuleStatus_RULE_STATUS_SUCCESS
	return r, nil
}

func Skip(r *pb.EvaluateResponse) (*pb.EvaluateResponse, error) {
	r.Status = pb.RuleStatus_RULE_STATUS_SKIP
	return r, nil
}

func Retry(r *pb.EvaluateResponse, t time.Time) (*pb.EvaluateResponse, error) {
	r.RetryTime = timestamppb.New(t)
	r.Status = pb.RuleStatus_RULE_STATUS_RETRY
	return r, nil
}
